# 🧠 AI-Powered Test Case Generation Project
The AI-Powered Test Case Generation Project is a comprehensive solution that leverages the power of artificial intelligence to generate test cases for software applications. This project combines the strengths of natural language processing, machine learning, and software development to provide a robust and efficient test case generation system. The project consists of two primary components: a client-side application built with Vue.js and a server-side application built with Django.

## 🚀 Features
- **AI-Powered Test Case Generation**: The project utilizes AI models to generate test cases based on input documents, reducing the time and effort required for manual test case creation.
- **Client-Side Application**: The client-side application provides a user-friendly interface for users to input documents and receive generated test cases.
- **Server-Side Application**: The server-side application handles the AI model interactions, test case generation, and storage of project configurations.
- **Project Configuration Management**: The project allows for the management of project configurations, enabling users to store and retrieve configuration settings.
- **User Authentication and Authorization**: The project includes user authentication and authorization mechanisms to ensure secure access to the application.

## 🛠️ Tech Stack
- **Frontend**:
  - Vue.js
  - Vue Router
  - Element UI
  - Axios
  - Dayjs
- **Backend**:
  - Django
  - Django REST Framework
  - PyMySQL
- **AI and Machine Learning**:
  - OpenAI
  - ZhiPu AI
- **Database**:
  - MySQL
- **Build Tools**:
  - Webpack
  - Webpack Merge

## 📦 Installation
To install the project, follow these steps:
1. Clone the repository using `git clone`.
2. Install the required dependencies for the client-side application using `npm install` or `yarn install`.
3. Install the required dependencies for the server-side application using `pip install -r requirements.txt`.
4. Configure the environment variables for the client-side and server-side applications.

## 💻 Usage
To use the project, follow these steps:
1. Start the client-side application using `npm run serve` or `yarn serve`.
2. Start the server-side application using `python manage.py runserver`.
3. Access the client-side application through a web browser.
4. Input a document and receive generated test cases.

## 📂 Project Structure
```markdown
client-ai/
├── public/
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   │   ├── index.js
│   ├── config/
│   │   ├── index.js
│   │   ├── prod.env.js
│   │   ├── dev.env.js
├── package.json
server_ai/
├── server_ai/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── models.py
├── server_func/
│   ├── views.py
│   ├── models.py
├── testcase_script/
│   ├── config.py
│   ├── call_my_model.py
│   ├── model.py
├── manage.py
requirements.txt
```

## 🤝 Contributing
To contribute to the project, please follow these steps:
1. Fork the repository using `git fork`.
2. Create a new branch using `git branch`.
3. Make changes and commit them using `git commit`.
4. Push the changes to the remote repository using `git push`.
5. Create a pull request to merge the changes into the main branch.
