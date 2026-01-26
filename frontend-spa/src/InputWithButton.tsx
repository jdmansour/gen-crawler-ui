import React, { useRef } from "react";
import ForwardIcon from "./assets/icons/arrow-forward.svg?react";
import "./InputWithButton.css";

export default function InputWithButton(
  props: {
    onAccept?: (value: string) => void;
  } & React.InputHTMLAttributes<HTMLInputElement>,
) {
  const input = useRef<HTMLInputElement>(null);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { onAccept, ...inputProps } = props;

  function accept() {
    if (input.current && props.onAccept) {
      props.onAccept(input.current.value);
    }
  }

  return (
    <div className="wlo-input-with-button">
      <input
        type="text"
        {...inputProps}
        ref={input}
        onKeyDown={(event) => event.key == "Enter" && accept()}
      />
      <button onClick={accept}>
        <ForwardIcon width={24} color="white" />
      </button>
    </div>
  );
}
