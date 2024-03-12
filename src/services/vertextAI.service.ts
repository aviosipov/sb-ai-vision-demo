import { VertexAI } from "@google-cloud/vertexai";
import fs from "fs";

let vertex_ai: VertexAI;
let generativeModel: any;

export const initializeVertexAI = () => {
  vertex_ai = new VertexAI({
    project: process.env.VERTEX_PROJECT_ID || "",
    location: process.env.VERTEX_LOCATION || "",
  });

  generativeModel = vertex_ai.preview.getGenerativeModel({
    model: "gemini-1.0-pro-vision-001",
    generation_config: {
      max_output_tokens: 2048,
      temperature: 0.4,
      top_p: 1,
      top_k: 32,
    },
  });
};

export const getImageCompletionVertex = async (imageFilePath: string, prompt: string) : Promise<string> => {

  const imageData = fs.readFileSync(imageFilePath);
  const base64Image = imageData.toString("base64");
    
  const req = {
    contents: [
      {
        role: "user",
        parts: [
          { inline_data: { mime_type: "image/png", data: base64Image } },
          {
            text: prompt,
          },
        ],
      },
    ],
  };

  const streamingResp = await generativeModel.generateContentStream(req);
  const response = await streamingResp.response;

  if (response && response.candidates && response.candidates.length > 0) {
    const textOutput = response.candidates[0].content.parts[0].text;
    return textOutput;
  } else {
    return "no text output found.";
  }
};
