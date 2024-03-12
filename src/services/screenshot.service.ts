import screenshot from "screenshot-desktop";
import sharp from "sharp";

export const takeScreenshot = (captureArea: {
  x: number;
  y: number;
  width: number;
  height: number;
}) => {
  return screenshot()
    .then((img: any) => {
      sharp(img)
        .extract({
          left: captureArea.x*2,
          top: captureArea.y*2,
          width: captureArea.width*2,
          height: captureArea.height*2,
        })
        .toFile("screenshot.png")
        .then(() => console.log("screenshot saved..."))
        .catch((err: any) => console.error("Error saving screenshot:", err));
    })
    .catch((err: any) => console.error("Error capturing screenshot:", err));
};
