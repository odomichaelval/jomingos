
# JOMINGOS Frontend

This is the frontend of the JOMINGOS project built with:

- Next.js
- React
- Bootstrap
- HTML
- CSS
- JavaScript

The project was originally designed using HTML, CSS, Bootstrap, and JavaScript before being converted into a Next.js application.

---

# Getting Started

Follow the steps below carefully to run this project successfully on your computer.

---

# Step 1 — Install Node.js

This project requires Node.js to run.

## Download Node.js

If node.js is not installed first install it.
Download windows installer.msi from node website https://nodejs.org/en/download. Install it at the default location. 


After installation, restart your computer.

---

# Step 2 — Verify Node.js Installation

Open your terminal or command prompt and run:

```bash
node -v
````

You should see a version number like:


v22.16.0 
(your version may be different depending on the latest available release).


# Step 3 — Clone the Project

Clone the repository from GitHub:

```bash
git clone GITHUB_REPOSITORY_LINK Or you download the file as zip and extract in your computer
```

Then move into the project folder:

```bash
cd frontend
```

---

# Step 4 — Install Project Dependencies


Run the command below to install all required dependencies:

```bash
npm install
```

Please wait patiently while installation completes.

---

# Step 5 — Important Fix for Memory Issues (Recommended)

If you copied the project from another folder or encounter memory crashes/errors, run the commands below before starting the project:

## Windows CMD

Delete old build cache:

```bash
rmdir /s /q .next
```

Delete dependencies:

```bash
rmdir /s /q node_modules
```

Delete lock file:

```bash
del package-lock.json
```

Then reinstall dependencies:

```bash
npm install
```

This helps prevent:

* Next.js crashes
* Browser freezing
* Out of memory errors
* Corrupted cache issues

---

# Step 6 — Run the Development Server

Start the project:

```bash
npm run dev
```

After successful startup, open:

```text
http://localhost:3000
```

in your browser.

---

# Additional Packages Used

This project uses additional animation libraries.

## AOS Animation Library

Install AOS:

```bash
npm install aos
```

Install AOS types:

```bash
npm install --save-dev @types/aos
```

---

## Swiper Slider Library

Install Swiper:

```bash
npm install swiper
```

---

# Common Errors & Solutions

## 1. Out of Memory Error

If you see errors like:

```text
Fatal process out of memory
```

Run:

```bash
rmdir /s /q .next
rmdir /s /q node_modules
del package-lock.json
npm install
```

Then restart the project.

---

## 2. Module Not Found Error

Example:

```text
Module not found: Can't resolve 'aos'
```

Install the missing package:

```bash
npm install aos
```

---

## 3. Port 3000 Already in Use

Close other running Node.js applications or restart your computer.

---

# Project Structure

```text
frontend/
│
├── app/
├── components/
├── lib/
├── public/
├── types/
├── package.json
└── README.md
```

---

# Learn More About Next.js

Useful resources:

* [Next.js Documentation](https://nextjs.org/docs?utm_source=chatgpt.com)
* [Learn Next.js](https://nextjs.org/learn?utm_source=chatgpt.com)
* [Next.js GitHub Repository](https://github.com/vercel/next.js?utm_source=chatgpt.com)

---

# Deploy on Vercel

The easiest way to deploy this Next.js app is using Vercel.

Deploy here:

[Deploy on Vercel](https://vercel.com/new?utm_source=chatgpt.com)

More deployment documentation:

[Next.js Deployment Documentation](https://nextjs.org/docs/app/building-your-application/deploying?utm_source=chatgpt.com)

```
```
