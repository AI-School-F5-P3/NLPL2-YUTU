from celery import Celery
import time

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def update_comments(video_id):
    comments = get_comments(video_id)
    results_df = classify_comments(comments)
    save_to_db(results_df, video_id)
    return "Comentarios actualizados"
