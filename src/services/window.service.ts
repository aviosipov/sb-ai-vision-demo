import { windowManager, Window } from "node-window-manager";

export const listWindows = () => {
  const windows = windowManager.getWindows();
  windows.forEach((win) => {
    console.log(` ${win.getTitle()}, ${win.id}  `);    
  });
};

export const getWindowById = (id: number) : Window | undefined => {
  const windows = windowManager.getWindows();
  return windows.find((win) => win.id === id);
};

export const focusOnWindowById = (id: number) => {
  const windows = windowManager.getWindows();
  const targetWindow = windows.find((win) => win.id === id);

  if (targetWindow) {
    targetWindow.bringToTop();
  } else {
    console.log("Window not found");
  }
};
