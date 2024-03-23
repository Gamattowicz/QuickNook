import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const alertVariants = cva(
  "relative w-full rounded-lg border px-4 py-3 text-sm [&>svg+div]:translate-y-[-33px] [&>svg]:absolute [&>svg]:left-3 [&>svg]:bottom-6 [&>svg]:text-foreground [&>svg~*]:pl-7",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground",
        primary:
          "bg-primary text-primary-foreground border-primary-foreground/50 dark:border-primary-foreground [&>svg]:text-primary-foreground",
        destructive:
          "bg-destructive text-destructive-foreground border-destructive-foreground/50 dark:border-destructive-foreground [&>svg]:text-destructive-foreground",
        secondary:
          "bg-secondary text-secondary-foreground border-secondary-foreground/50 dark:border-secondary-foreground [&>svg]:text-secondary-foreground",
        accent:
          "bg-accent text-accent-foreground border-accent-foreground/50 dark:border-accent-foreground [&>svg]:text-accent-foreground",
        muted:
          "bg-muted text-muted-foreground border-muted-foreground/50 dark:border-muted-foreground [&>svg]:text-muted-foreground",
        success:
          "bg-success text-success-foreground border-success-foreground/50 dark:border-success-foreground [&>svg]:text-success-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

const Alert = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof alertVariants>
>(({ className, variant, ...props }, ref) => (
  <div
    ref={ref}
    role="alert"
    className={cn(alertVariants({ variant }), className)}
    {...props}
  />
));
Alert.displayName = "Alert";

const AlertTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h5
    ref={ref}
    className={cn("mb-1 font-medium leading-none tracking-tight", className)}
    {...props}
  />
));
AlertTitle.displayName = "AlertTitle";

const AlertDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-sm [&_p]:leading-relaxed", className)}
    {...props}
  />
));
AlertDescription.displayName = "AlertDescription";

export { Alert, AlertTitle, AlertDescription };
