# 🚀 Quick Start - Google Drive Test

## מטרה
בדיקה מהירה שהעלאה ל-Google Drive עובדת מ-GitHub Actions

---

## ⚡ אופציה 1: בלי rclone במחשב (הכי פשוט!)

אם אתה לא רוצה להתקין rclone, אני אכין גרסה ש**לא צריכה שום דבר מהמחשב שלך**.

תגיד לי ואני אעבור לשיטה של Google Drive API שלא דורשת rclone כלל.

---

## ⚡ אופציה 2: עם rclone (מהיר יותר)

### שלב 1: בדיקה אם rclone כבר מותקן

פתח PowerShell והקלד:

```powershell
rclone version
```

**אם עובד** → עבור לשלב 2

**אם לא עובד** → אני אעזור להתקין (תגיד לי)

---

### שלב 2: הגדרת חיבור ל-Drive

הרץ:

```powershell
rclone config
```

**הוראות:**

1. `n` (new remote)
2. name: `gdrive-ollama`
3. Storage: `drive` (או המספר של Google Drive)
4. client_id: `Enter` (ריק)
5. client_secret: `Enter` (ריק)
6. scope: `1` (Full access)
7. service_account_file: `Enter` (ריק)
8. Edit advanced: `n`
9. Use web browser: `y`
10. **דפדפן ייפתח** → התחבר עם `s8001145@gmail.com`
11. לחץ **Allow**
12. חזור ל-PowerShell → `Enter`
13. Team drive: `n`
14. Confirm: `y`
15. Quit: `q`

---

### שלב 3: בדיקה שזה עובד

```powershell
rclone lsd gdrive-ollama:
```

אמור להראות את התיקיות שלך ב-Drive!

---

### שלב 4: שמירת ההגדרות

הרץ את הסקריפט:

```powershell
cd C:\Users\Koperberg\shidduch-ivr\ollama-models-downloader
.\setup_google_drive.ps1
```

זה יצור קובץ `rclone_gdrive_config.txt`

---

### שלב 5: הוספת Secret ל-GitHub

1. פתח: <https://github.com/sumca1/ollama-downloader/settings/secrets/actions>

2. לחץ **New repository secret**

3. מלא:
   - **Name**: `RCLONE_CONFIG`
   - **Value**: העתק הכל מהקובץ `rclone_gdrive_config.txt`

4. לחץ **Add secret**

---

### שלב 6: הרצת בדיקה

1. לך ל: <https://github.com/sumca1/ollama-downloader/actions>

2. בחר workflow: **Test Google Drive Upload**

3. לחץ **Run workflow**

4. הזן הודעה (אופציונלי)

5. לחץ **Run workflow**

---

## ✅ בדיקת תוצאות

אחרי 1-2 דקות:

1. פתח **Google Drive** שלך
2. חפש תיקייה: **Ollama-Test**
3. בפנים צריך להיות קובץ: **test-file.txt**
4. **הורד אותו** ובדוק שהתוכן נכון

**אם זה עובד** → המערכת מוכנה! נעבור למודלים של Ollama! 🎉

---

## ❓ בעיות?

**אם rclone לא מתקין:**
- תגיד לי ואני אעבור לשיטה ללא rclone

**אם ההרצה נכשלת:**
- העתק את השגיאה ואני אתקן

**אם הקובץ לא מופיע ב-Drive:**
- בדוק שהוספת את ה-Secret נכון
- בדוק שהתחברת עם `s8001145@gmail.com`
