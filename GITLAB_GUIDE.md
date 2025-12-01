# 🚀 GitLab CI/CD - הוראות שימוש

## 🎯 למה GitLab?

| תכונה | GitHub Actions | GitLab CI/CD |
|-------|---------------|--------------|
| 💾 **דיסק** | 14GB | **20GB** ✅ |
| 🧠 **RAM** | 7GB | **16GB** ✅ |
| ⏱️ **דקות חינמיות** | 2,000 | 400 |
| 📦 **Artifact גודל** | 2GB | 1GB |
| ✅ **נגיש בנטפרי** | כן | כן |

**תוצאה**: GitLab טוב יותר למודלים גדולים! 🎉

---

## שלב 1: יצירת חשבון GitLab

1. **גש ל-GitLab**: https://gitlab.com/users/sign_up

2. **הירשם**:
   - Email, Username, Password
   - אשר את המייל

3. **התחבר**: https://gitlab.com/users/sign_in

---

## שלב 2: יצירת Project ב-GitLab

### אופציה A: ייבוא מ-GitHub (מהיר!)

1. **גש ל**: https://gitlab.com/projects/new#import_project

2. **בחר "GitHub"**

3. **התחבר ל-GitHub** (אם נדרש)

4. **בחר את הproject**: `sumca1/ollama-models-downloader`

5. **לחץ "Import"**

6. **המתן** (~1 דקה)

---

### אופציה B: Push ידני (אם אופציה A לא עובדת)

1. **צור project חדש**: https://gitlab.com/projects/new

2. **מלא פרטים**:
   - Project name: `ollama-models-downloader`
   - Visibility: Public
   - **אל תאתחל** עם README

3. **בטרמינל**:

```powershell
# הוסף remote ל-GitLab
git remote add gitlab https://gitlab.com/YOUR_USERNAME/ollama-models-downloader.git

# דחף
git push gitlab main
```

---

## שלב 3: הרצת Pipeline

1. **גש לproject ב-GitLab**:
   ```
   https://gitlab.com/YOUR_USERNAME/ollama-models-downloader
   ```

2. **לחץ על "CI/CD" → "Pipelines"** (בתפריט השמאלי)

3. **לחץ "Run pipeline"** (כפתור כחול)

4. **הוסף Variables**:
   - לחץ "Add variable"
   - **Key**: `MODEL`
   - **Value**: `mistral:7b` (או `llama3.1:8b`)
   - לחץ "Run pipeline"

---

## שלב 4: מעקב אחר הריצה

1. **לחץ על הפייפליין** שזה עתה נוצר

2. **לחץ על "download_model"** - תראה לוג חי:
   ```
   🔍 Checking disk space...
   💾 Available space: 18G
   📦 Installing Ollama...
   🚀 Starting Ollama service...
   📥 Downloading model mistral:7b...
   ✅ Download complete!
   📦 Created 3 chunk(s)
   ✅ Model Export Complete!
   ```

3. **זמן המתנה**: ~10-15 דקות

---

## שלב 5: הורדת התוצאה

1. **אחרי שהריצה הסתיימה** (✅ סימן ירוק):

2. **בצד ימין**, תראה **"Job artifacts"**:
   ```
   📦 ollama-model-mistral:7b-XXX
   ```

3. **לחץ על "Download"** → בחר את כל הקבצים

4. **חלץ את ה-ZIP**

---

## שלב 6: התקנה

### אם מקטעים (part_aa, part_ab...):

#### Windows:
```powershell
cd ollama-models-export
.\reassemble.ps1
```

#### Linux/Mac:
```bash
cd ollama-models-export
chmod +x reassemble.sh
./reassemble.sh
```

### אם קובץ אחד (models.tar.gz):

#### Windows:
```powershell
cd ollama-models-export
tar -xzf models.tar.gz -C $env:USERPROFILE\.ollama\
```

#### Linux/Mac:
```bash
cd ollama-models-export
tar -xzf models.tar.gz -C ~/.ollama/
```

---

## שלב 7: בדיקה

```bash
ollama list
ollama run mistral:7b "מה המודל שלי?"
```

---

## 🎯 מודלים זמינים ב-GitLab

| מודל | גודל | יעבוד? |
|------|------|--------|
| mistral:7b | 4.1GB | ✅ בטוח |
| llama3.1:8b | 4.9GB | ✅ בטוח |
| llava:13b | 10GB | ✅ צריך לעבוד |
| codellama:34b | 20GB | ⚠️ על הגבול |
| llama3.1:70b | 40GB | ❌ גדול מדי |

---

## 🔄 הרצה מחדש

```
GitLab → CI/CD → Pipelines → Run pipeline
הוסף Variable: MODEL = llama3.1:8b
```

---

## 💡 טיפים

### 1. שמירת דקות
- 400 דקות/חודש = **~26 ריצות**
- כל מודל = ~15 דקות

### 2. ניהול Artifacts
- Artifacts נשמרים 7 ימים
- הורד מהר לפני שמחוקים!

### 3. Variables
- אפשר לשמור `MODEL` כ-CI/CD Variable קבוע
- Settings → CI/CD → Variables

---

## 🆚 GitLab vs GitHub - סיכום

**GitLab** מנצח עבור:
- ✅ מודלים גדולים (10-20GB)
- ✅ יותר RAM
- ✅ יותר דיסק

**GitHub** מנצח עבור:
- ✅ יותר דקות (2,000 vs 400)
- ✅ Artifacts גדולים יותר (2GB vs 1GB)

**המלצה**: השתמש בשניהם!
- GitHub → מודלים קטנים
- GitLab → מודלים בינוניים/גדולים

---

## 📞 עזרה

**בעיה**: Pipeline נכשל?
- בדוק את הלוג
- ודא ש-`MODEL` variable מוגדר
- נסה מודל קטן יותר

**בעיה**: אין artifacts?
- ודא שהריצה הסתיימה בהצלחה (✅)
- בדוק בצד ימין "Job artifacts"

---

**בהצלחה עם GitLab! 🚀**
