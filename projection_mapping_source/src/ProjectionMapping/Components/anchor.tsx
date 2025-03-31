import React from "react";
import { Anchor, Vector } from "./Keystoner";

const anchorSize = 20;
const halfAnchor = anchorSize / 1.5;
const vectorToTransform = (vector: Vector) =>
  `translate(${vector[0]}px, ${vector[1]}px)`;
const styles = {
  container: {
    width: anchorSize,
    height: anchorSize,
    borderRadius: "50%",
    position: "absolute" as "absolute",
    border: "2px solid white",
    cursor: "move",
    // fill color 50% transparent
    backgroundColor: "rgba(255, 0, 0, 0.5)",
  },
  "top-left": {
    left: -halfAnchor,
    top: -halfAnchor,
  },
  "bottom-left": {
    left: -halfAnchor,
    bottom: -halfAnchor,
  },
  "top-right": {
    top: -halfAnchor,
    right: -halfAnchor,
  },
  "bottom-right": {
    bottom: -halfAnchor,
    right: -halfAnchor,
  },
};

export interface Props {
  position: Anchor;
  onMouseEnter?: (position: Anchor) => void;
  // tslint:disable-next-line:no-any
  onMouseDown: (evt: any, position: Anchor) => void;
  onMouseUp: (position: Anchor) => void;
  translation: Vector;
  style?: React.CSSProperties;
  className?: string;
}

export const AnchorComponent = ({
  position,
  translation,
  onMouseEnter,
  onMouseDown,
  onMouseUp,
  className = "",
  style = {},
}: any) => (
  <div
    onMouseEnter={() => onMouseEnter && onMouseEnter(position)}
    onMouseDown={(evt) => onMouseDown(evt, position)}
    onMouseUp={() => onMouseUp(position)}
    className={className}
    style={{
      ...styles.container,
      ...styles[position],
      ...style,
      transform: vectorToTransform(translation),
    }}
  />
);
