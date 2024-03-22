import dotenv from 'dotenv';
dotenv.config();

import prompt from "prompt";
import { takeScreenshot } from "./services/screenshot.service";
import { getMousePosition, pressKey } from "./services/robot.service";
import {
  getImageCompletionVertex,
  initializeVertexAI,
} from "./services/vertextAI.service";
import { getWindowById, listWindows } from "./services/window.service";
import { getImageCompletionOpenAI } from './services/openAI.service';

let windowId = 10847;
const nextStepPrompt = `
in this game, the ball is falling down from the top of the screen.
to catch the ball in the game, i have to move right or left?    
reply only with "right or "left" 
`;


let window = getWindowById(windowId);
if (!window) {
  console.log("Window not found");
  listWindows();
  process.exit();
}

let bounds = window.getBounds();

initializeVertexAI();
prompt.start();

const takeGameStep = async () => {

  window?.bringToTop();

  await takeScreenshot({
    x: bounds.x || 0,
    y: bounds.y || 0,
    width: bounds.width || 0,
    height: bounds.height || 0,
  });

  // const nextStep = await getImageCompletionVertex("screenshot.png", nextStepPrompt);
  const nextStep = await getImageCompletionOpenAI("screenshot.png", nextStepPrompt);
  console.log(`suggested step: ${nextStep}`);
  pressKey(nextStep);
  
};

const autorunGameSteps = async (limit = 5) => {
  for (let i = 0; i < limit; i++) {
    console.log(`Running step ${i + 1}/${limit}`);
    await takeGameStep(); // Wait for the game step to complete before proceeding
  }
  console.log("Autorun complete.");
  
};


const showMenu = () => {
  console.log(`
  Choose an option:
  1 - Take game step
  2 - Get mouse position
  3 - Take a screenshot
  4 - Show windows
  5 - Run AI Vision query
  6 - Set windowId
  7 - Autorun 5 game steps
  Type 'exit' to quit.
  `);

  prompt.get(["option"], async function (err, result) {
    if (err) {
      return onErr(err);
    }
    switch (result.option) {
      case "1":
        await takeGameStep();
        showMenu();
        break;
      case "2":
        const mousePosition = getMousePosition();
        console.log(`Mouse position: ${mousePosition.x}, ${mousePosition.y}`);
        showMenu();
        break;
      case "3":
        await takeScreenshot({
          x: bounds.x || 0,
          y: bounds.y || 0,
          width: bounds.width || 0,
          height: bounds.height || 0,
        });
        showMenu();
        break;
      case "4":
        listWindows();
        showMenu();
        break;
      case "5":
        runAIVisionQuery();
        // showMenu();
        break;
      case "6":
        prompt.get(["newWindowId"], function (err, result) {
          if (err) {
            return onErr(err);
          }
          setWindowId(result.newWindowId as string);
        });
        break;

      case "7":
        await autorunGameSteps();
        showMenu();
        break;
  
      case "exit":
        console.log("Exiting...");
        process.exit();
        break;
      default:
        console.log("Invalid option.");
        showMenu();
        break;
    }
  });
};

const runAIVisionQuery = () => {
  prompt.get(["userPrompt"], async function (err, result) {
    if (err) {
      return onErr(err);
    }

    const response = await getImageCompletionOpenAI("screenshot.png", result.userPrompt as string)
    console.log(`AI Vision suggests: ${response}`);


    // getImageCompletionVertex("screenshot.png", result.userPrompt as string)
    //   .then((completion) => {
    //     console.log(`AI Vision suggests: ${completion}`);
    //   })
    //   .catch(onErr)
    //   .finally(showMenu);

    showMenu();
  });
};

const setWindowId = (newWindowId : string) => {
  windowId = parseInt(newWindowId, 10);
  const window = getWindowById(windowId);
  if (!window) {
    console.log("Window not found");
    listWindows();
  } else {
    console.log(`windowId set to ${windowId}`);
    bounds = window.getBounds(); // Ensure bounds are updated
  }
  showMenu();
};


const onErr = (err: any) => {
  console.log(err);
  return 1;
};

showMenu();
