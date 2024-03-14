import * as React from "react";

import { cn } from "@/lib/utils";
import { Input } from "./input";
import { EyeNoneIcon, EyeOpenIcon } from "@radix-ui/react-icons";

export interface PasswordInputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const PasswordInput = React.forwardRef<HTMLInputElement, PasswordInputProps>(
  ({ className, type, ...props }, ref) => {
    const [showPassword, setShowPassword] = React.useState(false);

    return (
      <div className="relative">
        <Input
          type={showPassword ? "text" : "password"}
          {...props}
          ref={ref}
          className={cn("pr-10", className)}
        />
        <span className="absolute top-[10px] right-4 cursor-pointer select-none">
          {showPassword ? (
            <EyeOpenIcon onClick={() => setShowPassword(false)} />
          ) : (
            <EyeNoneIcon onClick={() => setShowPassword(true)} />
          )}
        </span>
      </div>
    );
  }
);
PasswordInput.displayName = "PasswordInput";

export { PasswordInput };
