# 🚀 הוראות דחיפה ל-GitHub והרצה

## שלב 1: יצירת Repository חדש ב-GitHub

1. **גש ל-GitHub**: https://github.com/new

2. **הגדרות Repository**:
   - **Repository name**: `ollama-models-downloader`
   - **Description**: `🤖 Download Ollama AI models via GitHub Actions - bypass NetFree restrictions`
   - **Public/Private**: בחר לפי העדפה (מומלץ Public לשיתוף)
   - **DON'T** initialize with:
     - ❌ README (כבר יש לנו)
     - ❌ .gitignore (כבר יש לנו)
     - ❌ License (כבר יש לנו)

3. **לחץ "Create repository"**

---

## שלב 2: חיבור והעלאה

בטרמינל (בתיקיית הפרויקט):

```powershell
# הוסף את ה-remote (החלף YOUR_USERNAME בשם המשתמש שלך ב-GitHub)
git remote add origin https://github.com/YOUR_USERNAME/ollama-models-downloader.git

# שנה את שם ה-branch ל-main
git branch -M main

# דחף את הקוד
git push -u origin main
```

### דוגמה:
```powershell
# אם שם המשתמש שלך הוא: koperberg
git remote add origin https://github.com/koperberg/ollama-models-downloader.git
git branch -M main
git push -u origin main
```

---

## שלב 3: אימות Authentication (אם נדרש)

אם GitHub מבקש אימות:

### אופציה A: Personal Access Token (מומלץ)

1. גש ל: https://github.com/settings/tokens
2. לחץ **Generate new token (classic)**
3. בחר scopes:
   - ✅ `repo` (גישה מלאה לrepositories)
   - ✅ `workflow` (הרצת Actions)
4. העתק את ה-token
5. בפעם הבאה ש-git מבקש password, הדבק את ה-token

### אופציה B: GitHub CLI

```powershell
# התקנה
winget install GitHub.cli

# התחברות
gh auth login

# דחיפה
git push -u origin main
```

---

## שלב 4: עדכון README (אופציונלי)

ב-README.md, עדכן את השורה:

```markdown
[![Download Models](https://github.com/YOUR_USERNAME/ollama-models-downloader/actions/workflows/download-ollama-models.yml/badge.svg)](https://github.com/YOUR_USERNAME/ollama-models-downloader/actions/workflows/download-ollama-models.yml)
```

החלף `YOUR_USERNAME` בשם שלך.

לאחר מכן:
```powershell
git add README.md
git commit -m "Update badge with correct username"
git push
```

---

## שלב 5: הרצת GitHub Action

1. **גש ל-repository שלך ב-GitHub**

2. **לחץ על טאב "Actions"** (למעלה)

3. **בצד שמאל**, בחר **"Download Ollama Models (Offline Build)"**

4. **לחץ "Run workflow"** (כפתור כחול בצד ימין)

5. **בחר מודל**:
   - מומלץ להתחלה: `llama3.1:8b` (4.9GB, ~10 דקות)

6. **השאר chunk_size_mb**: `1900` (ברירת מחדל)

7. **לחץ "Run workflow"** (הכפתור הירוק)

---

## שלב 6: מעקב אחר ההורדה

1. תראה ריצה חדשה ברשימה
2. לחץ עליה לצפייה בלוג
3. תהליך:
   ```
   ✅ Install Ollama
   ✅ Start Ollama service
   📥 Downloading llama3.1:8b...
   ✅ Download complete!
   📦 Total size: 4987MB
   ⚡ No splitting needed
   ✅ Model Downloaded Successfully!
   ```

4. זמן המתנה: **~10-15 דקות** למודל קטן

---

## שלב 7: הורדת התוצאה

1. **אחרי שהריצה הסתיימה** (סימן ✅ ירוק)

2. **גלול למטה** בדף הריצה

3. **בסקציה "Artifacts"**, תראה:
   ```
   ollama-model-llama3.1:8b-XXX
   ```

4. **לחץ להוריד** (יוריד כ-ZIP)

5. **חלץ את הקובץ**

---

## שלב 8: התקנה במחשב שלך

### אם Ollama עדיין לא מותקן:
```powershell
# Windows
winget install Ollama.Ollama
```

### התקנת המודל:

#### אם קובץ אחד (models.tar.gz):
```powershell
cd ollama-model-*  # התיקייה שחילצת
tar -xzf models.tar.gz -C $env:USERPROFILE\.ollama\
```

#### אם מקטעים (part_aa, part_ab...):
```powershell
cd ollama-model-*
.\reassemble.ps1
```

#### או עם סקריפט Python:
```powershell
cd ollama-model-*
python ..\install_ollama_models.py .
```

---

## שלב 9: בדיקה

### בדיקת תקינות:
```powershell
python check_ollama_health.py
```

### בדיקת המודל:
```bash
ollama list
ollama run llama3.1:8b "שלום עולם!"
```

---

## 🎉 סיימת!

עכשיו יש לך:
- ✅ Repository ב-GitHub
- ✅ GitHub Action פעיל
- ✅ מודל AI מותקן
- ✅ יכולת להוריד מודלים נוספים

---

## 🔄 להוריד מודל נוסף

פשוט חזור ל:
```
GitHub → Actions → Download Ollama Models → Run workflow
```

ובחר מודל אחר!

---

## 📝 פקודות מהירות

```powershell
# בדיקת סטטוס Git
git status

# עדכון קובץ ו-push
git add .
git commit -m "Update README"
git push

# בדיקת מודלים
ollama list

# הרצת מודל
ollama run llama3.1:8b
```

---

**הצלחה! 🚀**
