# 🔑 Getting Your OpenAI API Key

This guide will help you get an OpenAI API key for the Fruit Classification System.

## Step 1: Create an OpenAI Account

1. Go to https://platform.openai.com/signup
2. Sign up with your email or Google/Microsoft account
3. Verify your email address

## Step 2: Add Payment Method (Required)

⚠️ **Important**: OpenAI requires a payment method even though they offer free credits.

1. Go to https://platform.openai.com/account/billing
2. Click "Add payment method"
3. Enter your credit/debit card details
4. New accounts get $5 in free credits (as of 2026)

## Step 3: Create API Key

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Give it a name (e.g., "Fruit Classifier")
4. Copy the key (starts with `sk-`)
   - ⚠️ **Save it now!** You won't be able to see it again

## Step 4: Add Key to Your Project

1. Open the `.env` file in your project
2. Replace `your-openai-api-key-here` with your actual key:
   ```
   OPENAI_API_KEY=sk-proj-abc123...
   ```
3. Save the file

## 💰 Pricing Information

### GPT-4 Vision (gpt-4o)
- **Input**: ~$2.50 per 1M tokens (~$0.0025 per image)
- **Output**: ~$10 per 1M tokens
- **Typical cost per classification**: $0.01 - $0.03

### Free Credits
- New accounts: $5 free credits
- Good for ~150-500 fruit classifications
- Valid for 3 months

### Usage Monitoring
Check your usage at: https://platform.openai.com/usage

## 🔒 Security Best Practices

1. **Never commit your API key to Git**
   - It's already in `.gitignore`
   - Don't share your `.env` file

2. **Use environment variables in production**
   ```bash
   export OPENAI_API_KEY=sk-your-key
   ```

3. **Set usage limits**
   - Go to: https://platform.openai.com/account/limits
   - Set monthly spending limits to avoid surprises

4. **Rotate keys regularly**
   - Create new keys periodically
   - Delete old/unused keys

## 🆘 Troubleshooting

### "Invalid API key" error
- Check for extra spaces or quotes in `.env`
- Verify the key starts with `sk-`
- Make sure you copied the entire key

### "Insufficient quota" error
- You've used all your free credits
- Add a payment method or purchase more credits
- Check usage: https://platform.openai.com/usage

### "Rate limit exceeded" error
- Too many requests too quickly
- Wait a minute and try again
- Consider upgrading your tier for higher limits

## 💡 Cost Optimization Tips

1. **Cache results**: Save common fruit classifications
2. **Batch requests**: Group multiple classifications if possible
3. **Set limits**: Configure spending limits in OpenAI dashboard
4. **Monitor usage**: Check your usage daily during testing
5. **Use cheaper models**: For testing, you could use `gpt-3.5-turbo` (not vision though)

## 🔄 Alternative: Free/Local Options

If you don't want to use OpenAI:

1. Set `USE_OPENAI=false` in `.env`
2. Train a local TensorFlow model (see README.md)
3. No API costs, but requires training data

## 📞 Support

- **OpenAI Help**: https://help.openai.com
- **API Status**: https://status.openai.com
- **Community**: https://community.openai.com

---

**Ready?** Once you have your API key, add it to `.env` and run:
```bash
python verify_setup.py  # Verify everything works
python backend/app.py   # Start the application
```
