# Google Drive Setup - Quick Test Guide

## 🎯 מטרה: בדיקת העלאה ל-Google Drive מ-Actions

**תהליך מהיר (10 דקות):**
1. התקנת rclone במחשב שלך
2. חיבור ל-Google Drive
3. העתקת הגדרות ל-GitHub/GitLab
4. הרצת בדיקה

---

## 📋 שלב 1: התקנת rclone

**Windows:**
1. הורד מ: <https://rclone.org/downloads/> (Windows AMD64)
2. חלץ את הקובץ
3. העתק `rclone.exe` ל: `C:\Windows\System32\`
4. פתח PowerShell חדש ובדוק: `rclone version`

**אם יש בעיה עם ההורדה (NetFree):**
- תגיד לי ואני אשלח לך דרך אחרת

---

## 📋 שלב 2: חיבור ל-Google Drive

1. **גש ל-Google Cloud Console**:
   - https://console.cloud.google.com/

2. **צור פרויקט חדש**:
   - לחץ על dropdown בפינה השמאלית העליונה
   - "NEW PROJECT"
   - שם: `ollama-models-uploader`
   - לחץ "CREATE"

---

## 📋 שלב 2: הפעלת Google Drive API

1. **בתוך הפרויקט**, לחץ על "APIs & Services" → "Library"

2. **חפש "Google Drive API"**

3. **לחץ "ENABLE"**

---

## 📋 שלב 3: יצירת Service Account

1. **לחץ על "APIs & Services" → "Credentials"**

2. **לחץ "CREATE CREDENTIALS" → "Service Account"**

3. **מלא פרטים**:
   - Service account name: `ollama-uploader`
   - Service account ID: (יתמלא אוטומטית)
   - לחץ "CREATE AND CONTINUE"

4. **בחר Role**: `Editor` (או השאר ריק)
   - לחץ "CONTINUE"
   - לחץ "DONE"

---

## 📋 שלב 4: יצירת JSON Key

1. **במסך Credentials**, תראה את ה-Service Account שיצרת

2. **לחץ על שם ה-Service Account**

3. **לשונית "KEYS"** → "ADD KEY" → "Create new key"

4. **בחר JSON** → "CREATE"

5. **קובץ JSON יורד למחשב שלך** - שמור אותו!

---

## 📋 שלב 5: שיתוף תיקייה ב-Drive

1. **פתח Google Drive** (https://drive.google.com/)
   - התחבר עם: `s8001145@gmail.com`

2. **צור תיקייה חדשה**:
   - שם מומלץ: `Ollama Models`

3. **שתף את התיקייה**:
   - לחץ ימני על התיקייה → "Share"
   - הוסף את כתובת המייל של ה-Service Account:
     - תמצא אותה בקובץ ה-JSON שהורדת
     - שדה: `client_email`
     - משהו כמו: `ollama-uploader@xxxxx.iam.gserviceaccount.com`
   - תן הרשאות: **Editor**
   - לחץ "Share"

4. **העתק את מזהה התיקייה**:
   - פתח את התיקייה ב-Drive
   - העתק את ה-ID מה-URL:
     ```
     https://drive.google.com/drive/folders/XXXXXXXXXXXXXXXXXXXXX
                                            ↑ זה ה-ID
     ```

---

## 📋 שלב 6: הוספת Secrets ל-GitHub/GitLab

### GitHub:
1. גש ל: https://github.com/sumca1/ollama-downloader/settings/secrets/actions

2. **הוסף 2 secrets**:

   **Secret 1:**
   - Name: `GDRIVE_SERVICE_ACCOUNT`
   - Value: העתק את **כל תוכן** קובץ ה-JSON שהורדת

   **Secret 2:**
   - Name: `GDRIVE_FOLDER_ID`
   - Value: מזהה התיקייה שהעתקת (השורה הארוכה)

### GitLab:
1. גש ל: https://gitlab.com/sumca1/ollama-models-downloader/-/settings/ci_cd

2. **הרחב "Variables"** → **Add variable** (פעמיים):

   **Variable 1:**
   - Key: `GDRIVE_SERVICE_ACCOUNT`
   - Value: העתק את **כל תוכן** קובץ ה-JSON
   - Type: Variable
   - Uncheck "Protect variable"
   - Check "Mask variable"

   **Variable 2:**
   - Key: `GDRIVE_FOLDER_ID`
   - Value: מזהה התיקייה
   - Type: Variable

---

## ✅ סיימת!

עכשיו ה-workflow יכול להעלות קבצים ישירות לתיקייה שלך ב-Google Drive!

**הקבצים יופיעו ב-Drive שלך תחת התיקייה "Ollama Models"** 🎉

---

## 🔍 בדיקה

אחרי שתוסיף את ה-secrets, תריץ workflow ותראה:
- ✅ קבצים מועלים ל-Google Drive שלך
- ✅ נגיש ישירות מהדרייב (ללא חסימת NetFree)
- ✅ אין מגבלת גודל של Actions
