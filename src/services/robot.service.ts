import robot from "robotjs";

export const pressKey = (key: string, duration: number = 250) => { // Default duration set to 100ms
  let robotKey: string;
  switch (key.toLowerCase().trim()) {
    case "up":
      robotKey = "w";
      break;
    case "down":
      robotKey = "s";
      break;
    case "left":
      robotKey = "a";
      break;
    case "right":
      robotKey = "d";
      break;
    default:
      console.log(`Invalid key: ${key}, allowed keys: up, down, left, right`);
      return;
  }
  
  robot.keyToggle(robotKey, 'down'); // Press the key down
  setTimeout(() => robot.keyToggle(robotKey, 'up'), duration); // Release the key after the duration
};

export const getMousePosition = (): { x: number, y: number } => {
  return robot.getMousePos();
};
