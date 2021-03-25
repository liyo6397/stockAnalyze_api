import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import info from "./components/forecast";

let container = null;
beforeEach(() => {
  // setup a DOM element as a render target
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  // cleanup on exiting
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});

it("renders user data", async () => {
  const info = {
    token: "GME",
    min_price: 158,
    max_price: 201,
    std: 6.25
  };
  jest.spyOn(global, "axios").mockImplementation(() =>
    Promise.resolve({
      json: () => Promise.resolve(info)
    })
  );

// Use the asynchronous version of act to apply resolved promises
  await act(async () => {
    render(<Forecast token="GME" />, container);
  });

  expect(container.querySelector("price").textContent).toBe(info.min_price);
  expect(container.querySelector("strong").textContent).toBe(info.max_price);
  expect(container.querySelector("h5")).toContain(info.token);

  // remove the mock to ensure tests are completely isolated
  global.fetch.mockRestore();

});