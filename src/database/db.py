from src.database.config import supabase
import bcrypt
from datetime import datetime, timezone



def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0 



def create_teacher(username, password, name, email=None):

    data = {"username": username, "password": hash_pass(password), "name": name, "email": email}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_teacher_by_email(email):
    response = supabase.table("teachers").select("teacher_id, username, email").eq("email", email).execute()
    return response.data[0] if response.data else None


def get_teacher_username(teacher_id):
    response = supabase.table("teachers").select("username").eq("teacher_id", teacher_id).single().execute()
    return response.data["username"] if response.data else None


def create_recovery_token(teacher_id, token_hash, token_type, expires_at):
    supabase.table("account_recovery_tokens").update({"used": True}).eq("teacher_id", teacher_id).eq("token_type", token_type).eq("used", False).execute()
    response = supabase.table("account_recovery_tokens").insert({
        "teacher_id": teacher_id,
        "token_hash": token_hash,
        "token_type": token_type,
        "expires_at": expires_at,
    }).execute()
    return response.data[0] if response.data else None


def get_valid_recovery_token(token_hash, token_type):
    response = supabase.table("account_recovery_tokens").select("id, teacher_id, expires_at").eq("token_hash", token_hash).eq("token_type", token_type).eq("used", False).execute()
    if not response.data:
        return None
    token = response.data[0]
    expires_at = datetime.fromisoformat(token["expires_at"].replace("Z", "+00:00"))
    return token if expires_at > datetime.now(timezone.utc) else None


def use_recovery_token(token_id):
    response = supabase.table("account_recovery_tokens").update({"used": True}).eq("id", token_id).eq("used", False).execute()
    return bool(response.data)


def update_teacher_password(teacher_id, password):
    response = supabase.table("teachers").update({"password": hash_pass(password)}).eq("teacher_id", teacher_id).execute()
    return bool(response.data)


def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


def  enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response= supabase.table('subject_students').insert(data).execute()
    return response.data


def  unenroll_student_to_subject(student_id, subject_id):
    response= supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data



def get_student_subjects(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data

