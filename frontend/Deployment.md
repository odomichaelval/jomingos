Step-by-Step Guide: Deploying a Next.js Frontend to Vercel
1. Prepare Your Next.js Project

Before deployment, ensure your project runs correctly locally.

Open terminal inside your project folder:

npm install

Then run:

npm run dev

Open:

http://localhost:3000

If the site works locally, proceed.

2. Push Your Project to GitHub
Initialize Git (if not already done)
git init
Add files
git add .
Commit files
git commit -m "Initial frontend deployment"
Create Repository on GitHub

Go to:

GitHub New Repository

Example repository name:

jomingos-frontend
Connect local project to GitHub

Replace YOUR_USERNAME below:

git remote add origin https://github.com/YOUR_USERNAME/jomingos-frontend.git
Push project
git branch -M main
git push -u origin main
3. Create a Vercel Account

Go to:

Vercel Official Website

Sign up using:

GitHub
Google
Email

Using GitHub is recommended.

4. Import Your GitHub Repository into Vercel

After login:

Click Add New
Click Project
Select your GitHub repository
Click Import
5. Configure Project Settings

Vercel automatically detects Next.js projects.

You should see:

Framework Preset: Next.js

Usually no extra configuration is needed.

6. Add Environment Variables (if needed)

If your frontend connects to your Django backend, add:

NEXT_PUBLIC_API_URL=https://jomingos.onrender.com

In Vercel:

Open Project
Go to Settings
Environment Variables
Add variable
7. Deploy the Project

Click:

Deploy

Vercel will:

install dependencies
build your Next.js app
deploy automatically

Deployment usually takes 1–3 minutes.

8. Access Your Live Website

After deployment, Vercel provides a live URL like:

https://jomingos-frontend.vercel.app

Your frontend is now live.

9. Connect Frontend to Django Backend

Your frontend can now communicate with your backend hosted on:

https://jomingos.onrender.com

Example API call:

fetch("https://jomingos.onrender.com/api/login/")

10. Automatic Redeployment

Every time you push new code to GitHub:

git add .
git commit -m "Updated frontend"
git push

Vercel automatically redeploys the site.

No manual upload needed.