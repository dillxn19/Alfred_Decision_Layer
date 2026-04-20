Dillan Haran

Alfred Assessment Team

Execution Decision Layer

19 April 2026

Here is the code for the Alfred Decision Engine. The main idea is that the system looks at a conversation and scores clarity and risk on a scale of 1 to 10. The AI model only handles reading the text and pulling out those numbers. Then regular code takes over to make the final choice. Doing it this way keeps things safe because the AI does not get to make the final call on its own.

For the prompt design I gave the AI a clear role and asked it to return a specific data format. This stops the app from breaking. If the system takes too long to reply or if a user forgets to include important details the code catches the error. It will then safely ask a clarifying question instead of doing something risky. As the assistant gets more powerful tools the code will need stricter rules to check for danger. Over the next six months I want to build a way for the system to learn from its mistakes and adjust its risk scores. I also want to make the app run faster for really simple tasks.