# nail-biting-detection-app
It's an app that detects the hand approaching the mouth (head), and warns about the bad habit of nail biting.

It also plots the timestamps with the duration of nail biting in a line chart.

## To detect without sending email
```
python app.py
```

## To detect and send email with screenshot attatched
```
python app.py <receiver-email>
```

### Give email and password when asked
```
Enter your email address: <your-email>
Enter your email password: <your-app-specific-password>
```

## Creating your App Specific Password
1. Go to "https://myaccount.google.com/apppasswords"
2. Connect with your email account
3. Select app > Mail
4. Select device > Windows Computer
5. Hit GENERATE
6. Save the 16-letter password, and insert it in the "Enter your email password" field.