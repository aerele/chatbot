# Chatbot Builder for Frappe and ERPNext

## Introduction

With the **Chatbot Builder**, organizations can easily automate responses to time-consuming and frequently asked questions. The process is simple: 

1. **Identify Common Questions**: List the repetitive questions that your team handles.
2. **Create Reply Templates**: Design templates with variables to customize responses.
3. **Connect Server Scripts**: Link each template to a server script that processes the response.

That’s it! The chatbot is ready to handle user queries. Users are identified by their username or phone number, and responses are personalized based on the template and server script combination.

## Supported Platforms

Currently, the chatbot integrates with **Telegram (TG)**, with support for **WhatsApp** and **Slack** coming soon.

## Chat Flow

You can visualize the chatbot conversation as a tree structure. Each branch represents a conversation, starting from the root (initial question) to the leaf (final response). Each node in the tree is a message linked to a template, which may contain variables. These variables are filled using custom functions or server scripts, making each conversation dynamic and interactive.


## Setup

### Installation
1. **Clone the Chatbot App**

   Run the following command to clone the Chatbot app into your bench's apps directory:

   ```bash
   bench get-app https://github.com/aerele/chatbot
   ```

2. **Install the App on Your Site**

   Install the Chatbot app on your Frappe site using:

   ```bash
   bench --site your-site-name install-app chatbot
   ```

   Replace `your-site-name` with the actual name of your Frappe site.

### Telegram Configuration
1. **Access Chatbot Setup**

   In your Frappe instance, navigate to **Chatbot Setup**.

2. **Configure Telegram Settings**

   - Click on the **Telegram** tab.
   - Enter your Telegram bot details, including the **Bot Token**.

3. **Set the Webhook URL**

   In the **Webhook URL** field, input the root URL of your site, for example:

   ```
   https://erp.yourcompany.com
   ```

   **Note:** Ensure your site URL is accessible over the internet and uses HTTPS, as required by Telegram.

### Add a Party Type
1. **Navigate to Chatbot Party Type**

   Go to **Chatbot Party Type** in your Frappe instance.

2. **Add Party Types**

   Add the party types you want the chatbot to manage, such as **Employee**, **Customer**, or **Supplier**.

3. **Update Party Doctype**

   Upon adding a party type, a new tab with a field for the Telegram username will be added to the corresponding party doctype. This allows you to input the Telegram username for each party, enabling personalized interactions.

You are now ready to design your **Chatbot Flow** and start automating your interactions with users.

