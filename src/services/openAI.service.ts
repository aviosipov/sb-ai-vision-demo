import OpenAI from "openai";
import fs from "fs";

const openai = new OpenAI();

export const getImageCompletionOpenAI = async (
  imageFilePath: string,
  prompt: string
): Promise<string> => {

  const imageData = fs.readFileSync(imageFilePath);
  const base64Image = imageData.toString("base64");

  const response = await openai.chat.completions.create({
    model: "gpt-4-vision-preview",
    messages: [
      {
        role: "user",
        content: [
          { type: "text", text: prompt },
          {
            type: "image_url",
            image_url: {
              url: `data:image/jpeg;base64,${base64Image}`,
            },
          },
        ],
      },
    ],
  });

  

  if (response && response.choices && response.choices.length > 0) {
    let textOutput = "";
    for (const choice of response.choices) {
      if (choice.message && choice.message.content) {
        if (Array.isArray(choice.message.content)) {
          textOutput += choice.message.content.map((item) => item.text).join("");
        } else {
          textOutput += choice.message.content;
        }
      }
    }
    return textOutput;
  } else {
    return "No text output found.";
  }
};
