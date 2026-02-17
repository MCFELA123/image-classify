# 🚀 Quick Start Guide

Get your Fruit Classification System running in 5 minutes!

## Prerequisites

You'll need:
- Python 3.8+
- MongoDB
- **OpenAI API Key** (get one at https://platform.openai.com/api-keys)

## Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy your API key (starts with `sk-`)
5. **Keep it secure!**

## Step 1: Install MongoDB

### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

Windows: Download from https://www.mongodb.com/try/download/community

## Step 2: Install MongoDB

```bash
# Navigate to project directory
cd "/Users/michaelchibuzor/Desktop/image classification project"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Set Up Python Environment

```bash
# Navigate to project directory
cd "/Users/michaelchibuzor/Desktop/image classification project"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Configure OpenAI API Key

```bash
# Copy environment template
cp .env.example .env
```

**IMPORTANT:** Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

You can edit the file with:
```bash
nano .env
# or
open .env  # macOS
```

## Step 5: Run the Application

### Option A: Using the run script (macOS/Linux)
```bash
./run.sh
```

### Option B: Manual start
```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
python backend/app.py
```

## Step 6: Open in Browser

Visit: **http://localhost:5000**

## 🎯 Testing the Application

1. **Upload an image**
   - Click the upload area or drag & drop a fruit image
   - Supports: JPG, PNG, GIF (max 16MB)

2. **Classify**
   - Click "Classify Image" button
   - View prediction results with confidence scores

3. **Explore features**
   - View classification history
   - Check statistics dashboard

## 🧪 Test the API

```bash
# Test API endpoints
python test_api.py

# Test with a specific image
python test_api.py path/to/fruit-image.jpg
```

## 📊 Training Your Own Model

To train with your own fruit images:

1. **Organize your dataset:**
```
training_data/
├── Apple/
│   ├── apple1.jpg
│   ├── apple2.jpg
│   └── ...
├── Banana/
│   └── ...
└── ...
```

2. **Train the model:**
```bash
python train.py --train-dir training_data --epochs 20
```

## 🐛 Troubleshooting

### "OpenAI API key is required" error
- Make sure you added your API key to `.env`
- Check the key starts with `sk-`
- Verify no extra spaces in the `.env` file

### "Import openai could not be resolved"
```bash
source venv/bin/activate
pip install openai
```

### MongoDB won't start
```bash
# Check MongoDB status
brew services list  # macOS
sudo systemctl status mongodb  # Linux

# Restart MongoDB
brew services restart mongodb-community  # macOS
sudo systemctl restart mongodb  # Linux
```

### Port 5000 already in use
Edit `backend/app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module not found errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### TensorFlow installation issues
Not needed anymore! We use OpenAI instead.

### Rate limit errors from OpenAI
- You've hit your API usage limit
- Wait a few minutes
- Check your usage at platform.openai.com
- Consider adding billing/upgrading your plan

## 💰 Cost Information

- Each classification costs approximately $0.01-0.03
- OpenAI offers $5 free credits for new accounts
- Monitor usage at https://platform.openai.com/usage

## 📚 Available Fruit Classes

The system can classify these fruits:
1. Apple 🍎
2. Banana 🍌
3. Orange 🍊
4. Mango 🥭
5. Strawberry 🍓
6. Grape 🍇
7. Watermelon 🍉
8. Pineapple 🍍
9. Cherry 🍒
10. Kiwi 🥝

## 🎨 Customization

### Add more fruit classes:
Edit `backend/config.py`:
```python
FRUIT_CLASSES = [
    'Apple', 'Banana', 'Orange', ..., 'YourNewFruit'
]
```

No retraining needed with OpenAI! Just update the list.

### Switch to local model (no OpenAI):
Edit `.env`:
```
USE_OPENAI=false
```
Then train a local model (see README.md).

### Modify upload limits:
Edit `.env`:
```
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
```

## 📖 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [API documentation](README.md#-api-documentation)
- Monitor your OpenAI usage and costs
- Explore advanced features

## 💡 Tips

- **Better images = better results**: Use clear, well-lit photos
- **Monitor costs**: Check your OpenAI dashboard regularly
- **Cache results**: Consider saving common classifications to reduce API calls
- **Test thoroughly**: Try different fruits and image qualities

## 🆘 Need Help?

Check the full README.md for:
- Detailed API documentation
- Model architecture details
- Production deployment guide
- Advanced configuration options

---

**Happy Classifying! 🍎🍌🍊**
