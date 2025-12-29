# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import IChing  # 引入你之前写的 IChing 类
# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import IChing  # 引入你之前写的 IChing 类
import io
import sys

app = FastAPI()

# 允许跨域请求 (为了让前端网页能访问后端接口)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义前端发送的数据格式
class DivinationRequest(BaseModel):
    question: str = ""

# 初始化你的占卜系统 (默认关闭 verbose，以便网页端按需开启)
# 注意：确保 Ollama 已经在后台运行
iching_system = IChing(
    ollama_url="http://localhost:11434",
    model="qwen3:4b",
    verbose=False,  # 默认关闭详细打印
    concise=True    # 使用精简模式，适合网页展示
)


@app.get("/")
def read_root():
    return {"status": "周易占卜API正在运行"}


@app.post("/api/divine")
def create_divination(request: DivinationRequest):
    """
    接收前端的问题，调用 IChing 系统，并捕获起卦时的控制台输出（完整过程），返回结果和日志
    """
    try:
        # 1. 检查 Ollama 连接
        if not iching_system.ollama.check_connection():
            raise HTTPException(status_code=503, detail="无法连接到 AI 服务 (Ollama)，请检查服务是否开启。")

        # 2. 为了在网页端看到起卦全过程，我们临时启用 verbose 并捕获 stdout
        original_verbose = iching_system.verbose
        original_div_verbose = iching_system.divination.verbose
        iching_system.verbose = True
        iching_system.divination.verbose = True

        buf = io.StringIO()
        old_stdout = sys.stdout
        chunks = []
        try:
            sys.stdout = buf
            # 使用流式方式，按主程序运行顺序输出并捕获控制台字符
            gen = iching_system.divine(question=request.question, stream=True)
            # 消费生成器，主程序在控制台是边打印边消费，这里复现相同行为并收集所有chunk
            for chunk in gen:
                try:
                    # chunk 已是清理后的文本片段，按顺序追加
                    chunks.append(chunk)
                except Exception:
                    # 忽略单个片段错误，继续
                    pass
        finally:
            # 恢复状态
            sys.stdout = old_stdout
            iching_system.verbose = original_verbose
            iching_system.divination.verbose = original_div_verbose

        log = buf.getvalue()
        result_text = ''.join(chunks)

        return {
            "success": True,
            "question": request.question,
            "result": result_text,
            "log": log
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    # 启动服务器，端口 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)