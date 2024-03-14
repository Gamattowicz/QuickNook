type Props = {
  children?: React.ReactNode;
};

export default function AuthLayout({ children }: Props) {
  return (
    <>
      <div className="flex flex-col gap-4 min-h-screen items-center justify-center p-4">
        {children}
      </div>
    </>
  );
}
