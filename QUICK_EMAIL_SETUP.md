# Quick Email Setup Guide

**No cloud service provider needed!** You can use Gmail's free SMTP service.

## Simple Gmail Setup (5 minutes)

### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification" if not already enabled

### Step 2: Generate App Password
1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
   - Or: Google Account → Security → 2-Step Verification → App passwords
2. Select "Mail" as the app
3. Select "Other (Custom name)" as device, enter "Exam Grader"
4. Click "Generate"
5. **Copy the 16-character password** (you won't see it again!)

### Step 3: Add to .env File
Add these lines to your `.env` file in the project root:

```env
# Email Configuration (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_USE_TLS=true
```

**Important:**
- Replace `your-email@gmail.com` with your actual Gmail address
- Replace `xxxx xxxx xxxx xxxx` with the 16-character app password (you can include or remove spaces)
- Use the **app password**, NOT your regular Gmail password

### Step 4: Restart Your Application
Restart the FastAPI server for the changes to take effect.

## Testing

1. Dispute a grade as a student
2. Check the application logs - you should see:
   - `Email sent successfully to instructor@email.com: ...` (success)
   - OR `Email not configured - SMTP credentials missing...` (needs setup)
   - OR `SMTP Authentication failed...` (wrong password)

## Troubleshooting

### "Email not configured" warning
- Check that all SMTP_* variables are in your `.env` file
- Make sure there are no typos in variable names
- Restart the application after adding variables

### "SMTP Authentication failed"
- Make sure you're using an **App Password**, not your regular Gmail password
- Verify 2-Factor Authentication is enabled
- Check that the email address matches exactly

### "Connection refused" or "Connection timeout"
- Check your internet connection
- Verify SMTP_HOST and SMTP_PORT are correct
- Some networks block SMTP ports - try a different network

## Alternative: Other Email Providers

### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
SMTP_FROM_EMAIL=your-email@outlook.com
SMTP_USE_TLS=true
```

### Yahoo
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@yahoo.com
SMTP_USE_TLS=true
```

## Cloud Services (Optional)

If you prefer a dedicated email service:
- **SendGrid**: Free tier (100 emails/day)
- **Mailgun**: Free tier (5,000 emails/month)
- **AWS SES**: Pay-as-you-go

These require API keys instead of SMTP credentials, but would need code changes to implement.
