from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .api.routes import auth, courses, categories, sections, lessons, enrollment, progress
from .subscribers.payment_subscriber import start_payment_success_listener, stop_payment_success_listener

app = FastAPI(title="CodeCamp Core Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(categories.router)
app.include_router(sections.router)
app.include_router(lessons.router)
app.include_router(enrollment.router)
app.include_router(progress.router)


@app.on_event("startup")
async def startup_event():
    await start_payment_success_listener()


@app.on_event("shutdown")
async def shutdown_event():
    await stop_payment_success_listener()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)