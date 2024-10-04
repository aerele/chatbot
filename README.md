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
