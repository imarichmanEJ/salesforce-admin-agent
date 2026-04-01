from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from agent.agent import graph

app = FastAPI(title="SF Guide Agent")
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    types: list[str] = []
    steps: list[str] = []
    reasoning: str = ""
    error: str | None = None


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": req.session_id}}

    result = graph.invoke(
        {"messages": [HumanMessage(content=req.message)]},
        config=config,
    )

    # 에러 확인
    error = result.get("error")
    if error:
        return ChatResponse(
            session_id=req.session_id,
            reply=f"오류가 발생했습니다: {error}",
            error=error,
        )

    return ChatResponse(
        session_id=req.session_id,
        reply=result.get("guide", ""),
        types=result.get("types") or [],
        steps=result.get("steps") or [],
        reasoning=result.get("reasoning") or "",
    )


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    return {"status": "cleared"}