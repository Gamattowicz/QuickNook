import React from "react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { CircleAlert, CircleCheck, CircleHelp } from "lucide-react";

interface MessageProps {
  variant:
    | "default"
    | "primary"
    | "destructive"
    | "accent"
    | "muted"
    | "success"
    | "secondary";
  title: string;
  description: string;
}
export default function Message({ variant, title, description }: MessageProps) {
  const Icon =
    variant === "destructive"
      ? CircleAlert
      : variant === "success"
      ? CircleCheck
      : CircleHelp;

  return (
    <div className="w-full max-w-sm">
      <Alert variant={variant}>
        <Icon className="h-5 w-5" />
        <AlertTitle>{title}</AlertTitle>
        <AlertDescription>{description}</AlertDescription>
      </Alert>
    </div>
  );
}
