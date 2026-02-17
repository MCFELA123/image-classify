# 🍎 AI-Based Fruit Classification System

An intelligent fruit classification system powered by **OpenAI's GPT-4 Vision API** that can identify and classify different types of fruits from images with high accuracy.

## 🌟 Features

### Core Classification
- **OpenAI GPT-4 Vision**: Leverages state-of-the-art AI for accurate fruit identification
- **10 Fruit Categories**: Apple, Banana, Orange, Mango, Strawberry, Grape, Watermelon, Pineapple, Cherry, Kiwi
- **Real-time Predictions**: Instant classification with confidence scores and reasoning
- **History Tracking**: MongoDB database stores all classification results
- **Statistics Dashboard**: View classification trends and distribution
- **Modern UI**: Clean, minimalist interface inspired by Vercel's design
- **REST API**: Well-documented API endpoints for integration
- **No Training Required**: Uses OpenAI's pre-trained models

### 🆕 Fruit Quality & Ripeness Detection
- **Ripeness Detection**: Classifies fruits as unripe, ripe, or overripe
- **Spoilage Detection**: Identifies damaged, bruised, or spoiled fruits
- **Quality Scoring**: 0-100 quality score with edibility assessment

### 🆕 Disease & Defect Detection
- **Defect Identification**: Detects bruises, rot, mold, discoloration, cuts, blemishes
- **Disease Detection**: Identifies visible fruit diseases and spots
- **Health Assessment**: Outputs whether fruit is healthy or defective

### 🆕 Weight, Size & Grading System
- **Size Estimation**: Classifies as small, medium, large, extra-large
- **Weight Estimation**: Estimates weight based on visual analysis
- **Quality Grading**: A (Premium), B (Standard), C (Economy) grades
- **Pricing Calculation**: Price multipliers for packaging and retail

### 🆕 Smart Agriculture Integration
- **Farm Management Export**: Export data for FMS systems
- **Inventory Reporting**: Generate inventory summaries
- **Webhook Notifications**: Real-time alerts for external systems
- **API Schema**: OpenAPI-compatible integration documentation

### 🆕 Security & Privacy
- **Auto Image Cleanup**: Temporary storage with automatic deletion
- **Privacy Compliance**: GDPR-ready data handling
- **Ethical Guidelines**: Documented AI ethics for agriculture

### 🆕 Performance Evaluation
- **Accuracy Metrics**: Precision, recall, F1-score calculation
- **Confusion Matrix**: Detailed prediction analysis
- **Limitations Documentation**: Clear system constraints

## 🏗️ Project Structure

```
image classification project/
├── backend/
│   ├── models/
│   │   ├── fruit_classifier.py       # CNN model implementation
│   │   ├── enhanced_analyzer.py      # Full analysis with ripeness/quality
│   │   ├── openai_classifier.py      # OpenAI Vision API
│   │   ├── agriculture_integration.py # 🆕 Farm management integration
│   │   ├── grading_system.py         # 🆕 Size/weight/grading
│   │   ├── security_privacy.py       # 🆕 Privacy compliance
│   │   ├── performance_evaluation.py # 🆕 Metrics & evaluation
│   │   ├── nutrition_database.py     # Nutritional information
│   │   ├── multilingual.py           # Language support
│   │   └── database.py               # MongoDB handler
│   ├── routes/
│   │   └── api.py                    # API endpoints (40+ routes)
│   ├── utils/
│   │   └── image_utils.py            # Image processing utilities
│   ├── app.py                        # Flask application
│   └── config.py                     # Configuration settings
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css             # Styles
│   │   └── js/
│   │       └── app.js                # Frontend logic
│   └── index.html                    # Main HTML page
├── data/
│   └── uploads/                      # Uploaded images storage
├── trained_models/                   # Saved model files
├── requirements.txt                  # Python dependencies
├── ADVANCED_FEATURES.md              # 🆕 Advanced features documentation
├── ARCHITECTURE.md                   # System architecture
├── .env.example                      # Environment variables template
└── README.md                         # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MongoDB 4.4 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "/Users/michaelchibuzor/Desktop/image classification project"
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```
   
   **Important:** Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```
   
   Get your API key from: https://platform.openai.com/api-keys

5. **Install and start MongoDB**
   
   On macOS:
   ```bash
   brew tap mongodb/brew
   brew install mongodb-community
   brew services start mongodb-community
   ```
   
   On Linux:
   ```bash
   sudo apt-get install mongodb
   sudo systemctl start mongodb
   ```
   
   On Windows: Download from [MongoDB website](https://www.mongodb.com/try/download/community)

### Running the Application

**Important:** Make sure you have added your OpenAI API key to the `.env` file before starting!

1. **Start the Flask server**
   ```bash
   python backend/app.py
   ```

2. **Open your browser**
   ```
   http://localhost:5000
   ```

The application will be running at `http://localhost:5000`

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "classifier_loaded": true,
  "database_connected": true,
  "using_openai": true
}
```

#### 2. Classify Image
```http
POST /api/classify
Content-Type: multipart/form-data
```

Parameters:
- `image`: Image file (JPG, PNG, GIF)

Response:
```json
{
  "classification_id": "507f1f77bcf86cd799439011",
  "predicted_class": "Apple",
  "confidence": "95.5%",
  "confidence_raw": 0.955,
  "top_predictions": [
    {
      "class": "Apple",
      "confidence": "95.5%",
      "confidence_raw": 0.955
    },
    {
      "class": "Cherry",
      "confidence": "3.2%",
      "confidence_raw": 0.032
    },
    {
      "class": "Strawberry",
      "confidence": "1.3%",
      "confidence_raw": 0.013
    }
  ],
  "image_filename": "apple_20260210_143022.jpg",
  "reasoning": "The image clearly shows a red apple with characteristic round shape and stem"
}
```

#### 3. Get History
```http
GET /api/history?limit=20
```

Response:
```json
{
  "count": 20,
  "history": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "image_filename": "apple_20260210_143022.jpg",
      "predicted_class": "Apple",
      "confidence": 0.955,
      "timestamp": "2026-02-10T14:30:22.000Z"
    }
  ]
}
```

#### 4. Get Classification by ID
```http
GET /api/history/{classification_id}
```

#### 5. Get Statistics
```http
GET /api/statistics
```

Response:
```json
{
  "total_classifications": 150,
  "class_counts": {
    "Apple": 45,
    "Banana": 32,
    "Orange": 28,
    "Mango": 20,
    "Strawberry": 15,
    "Grape": 10
  }
}
```

#### 6. Get Available Classes
```http
GET /api/classes
```

Response:
```json
{
  "classes": ["Apple", "Banana", "Orange", "Mango", "Strawberry", "Grape", "Watermelon", "Pineapple", "Cherry", "Kiwi"],
  "count": 10
}
```

### 🆕 New Advanced Endpoints

#### Grading System
```http
POST /api/grading/estimate-size      # Estimate fruit size
POST /api/grading/estimate-weight    # Estimate fruit weight
POST /api/grading/calculate-grade    # Calculate quality grade (A/B/C)
POST /api/grading/packaging          # Get packaging recommendations
POST /api/grading/batch              # Grade multiple fruits
```

#### Smart Agriculture Integration
```http
GET  /api/integration/export         # Export classification data
GET  /api/integration/inventory      # Get inventory report
GET  /api/integration/farm-export    # Farm management system export
POST /api/integration/pricing        # Calculate pricing
POST /api/integration/webhook        # Register webhook
GET  /api/integration/schema         # Get API schema (OpenAPI)
```

#### Security & Privacy
```http
GET    /api/privacy/policy           # Full privacy policy
GET    /api/privacy/ethical-guidelines # AI ethics documentation
POST   /api/privacy/cleanup          # Manual image cleanup
DELETE /api/privacy/delete-data      # Delete user data (GDPR)
```

#### Performance Evaluation
```http
GET  /api/evaluation/metrics         # Available metrics
POST /api/evaluation/evaluate        # Evaluate predictions
GET  /api/evaluation/limitations     # System limitations
GET  /api/evaluation/report          # Generate full report
```

> 📖 **For complete documentation of all new endpoints, see [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)**

## 🤖 Using OpenAI for Classification

This system uses OpenAI's GPT-4 Vision API for intelligent fruit classification:

### Benefits:
- ✅ **No training required** - Works immediately with pre-trained AI
- ✅ **High accuracy** - Leverages OpenAI's advanced vision capabilities
- ✅ **Natural language reasoning** - Provides explanations for classifications
- ✅ **Easy to update** - Add new fruit categories without retraining
- ✅ **Robust** - Handles various image qualities and angles

### Cost Considerations:
- OpenAI charges per API call (see [pricing](https://openai.com/pricing))
- Typical cost: ~$0.01-0.03 per image classification
- Consider caching results for repeated images
- Monitor usage in your OpenAI dashboard

### Alternative: Local Model
If you prefer not to use OpenAI, you can switch to a local TensorFlow model:

1. Set `USE_OPENAI=false` in `.env`
2. Train a local model (see Training section below)
3. The system will automatically use the local model

## 🎯 Training a Local Model (Optional)

If you want to use a local model instead of OpenAI:

1. **Prepare your dataset**
   - Organize images in folders by class name
   - Structure: `training_data/Apple/`, `training_data/Banana/`, etc.

2. **Train the model**
   ```python
   from backend.models.fruit_classifier import FruitClassificationModel
   
   model = FruitClassificationModel(num_classes=10, image_size=224)
   model.build_model()
   
   history = model.train_model(
       train_data_dir='path/to/training_data',
       epochs=20,
       batch_size=32
   )
   
   model.save_model('trained_models/fruit_classifier.h5')
   ```

3. **Use pre-trained weights**
   - The model uses MobileNetV2 pre-trained on ImageNet
   - Transfer learning allows for quick adaptation to fruit images

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **OpenAI API**: GPT-4 Vision for image classification
- **MongoDB**: Database for storing classifications
- **PyMongo**: MongoDB driver
- **Pillow**: Image processing

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Vanilla JavaScript**: No frameworks, lightweight
- **Fetch API**: HTTP requests
- **CSS Grid/Flexbox**: Responsive layout

### AI & Machine Learning
- **OpenAI GPT-4 Vision**: Primary classification engine
- **Base64 Encoding**: Image transmission to API
- **JSON Parsing**: Structured AI responses
- **Optional TensorFlow/Keras**: For local model fallback

## 📊 System Architecture

```
User Upload
    ↓
Flask API (backend/routes/api.py)
    ↓
OpenAI GPT-4 Vision API
    ↓
Classification Result
    ↓
MongoDB Storage (backend/models/database.py)
    ↓
Response to User
```

**OpenAI Classification Flow:**
1. User uploads fruit image
2. Image encoded to base64
3. Sent to GPT-4 Vision with classification prompt
4. AI analyzes image and returns structured JSON
5. Results validated and normalized
6. Saved to MongoDB
7. Displayed to user with confidence scores

## 🎨 UI Features

- **Drag & Drop**: Intuitive image upload
- **Live Preview**: See your image before classification
- **Responsive Design**: Works on desktop and mobile
- **Dark Mode Ready**: Easy to customize
- **Smooth Animations**: Modern transitions and effects
- **Toast Notifications**: User-friendly feedback

## 🔧 Configuration

Edit `.env` file to customize:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=fruit_classification_db

# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=data/uploads
MAX_CONTENT_LENGTH=16777216

# OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
USE_OPENAI=true

# Local Model (if USE_OPENAI=false)
MODEL_PATH=trained_models/fruit_classifier.h5
IMAGE_SIZE=224
```

## 📝 Notes

- **OpenAI API Key Required**: You need a valid OpenAI API key to use the classification feature
- **API Costs**: Each classification uses the OpenAI API and incurs a small cost
- **Rate Limits**: OpenAI has rate limits; monitor your usage
- **Alternative**: Can switch to local TensorFlow model by setting `USE_OPENAI=false`
- **Storage**: MongoDB stores classification history; configure data retention as needed
- **Image Quality**: Better quality images generally produce more accurate results

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
brew services list  # macOS
sudo systemctl status mongodb  # Linux

# Start MongoDB
brew services start mongodb-community  # macOS
sudo systemctl start mongodb  # Linux
```

### Module Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### OpenAI API Errors
```bash
# Check your API key in .env
# Verify at: https://platform.openai.com/api-keys

# Test connection
python backend/models/openai_classifier.py
```

### Rate Limit Errors
If you hit OpenAI rate limits:
- Wait a few moments before retrying
- Check your usage limits at platform.openai.com
- Consider upgrading your OpenAI plan

### Port Already in Use
```bash
# Change port in backend/app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 🚀 Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Secure your OpenAI API key (use environment variables)
3. Use a production WSGI server (Gunicorn)
4. Set up reverse proxy (Nginx)
5. Configure MongoDB with authentication
6. Enable HTTPS with SSL certificates
7. Set up monitoring for API usage and costs

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Created with ❤️ using Python, TensorFlow, and Flask

## 🙏 Acknowledgments

- OpenAI for GPT-4 Vision API
- Flask community
- MongoDB
- All open-source contributors

---

**Happy Classifying! 🍎🍌🍊**
