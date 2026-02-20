from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from routers import auth, scripts, chat, system

# 获取应用配置
settings = get_settings()

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="高情商聊天助手 - 专为研发团队打造的话术助手"
)

# 配置CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)    # 认证相关路由
app.include_router(scripts.router) # 话术脚本路由
app.include_router(chat.router)    # 聊天相关路由
app.include_router(system.router)  # 系统相关路由


@app.get("/")
async def root():
    """
    根路径接口
    返回API基本信息和文档链接
    """
    return {
        "message": "VibeCoding高情商聊天助手 API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup_event():
    """
    应用启动事件
    打印启动信息和文档地址
    """
    print(f"{settings.APP_NAME} 启动成功！")
    print(f"API文档地址: http://localhost:8000/docs")


if __name__ == "__main__":
    import uvicorn
    # 运行开发服务器
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
