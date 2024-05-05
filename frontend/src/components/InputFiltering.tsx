import React from 'react'
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

interface InputFilteringProps {
  placeholder: string;

  value: string;
  filterType: string;
  onChange: (value: React.ChangeEvent<HTMLInputElement>) => void;
}

export function InputFiltering({
  placeholder,
  value,
  filterType,
  onChange
}: InputFilteringProps) {

  return (
    <section className="grid w-full max-w-sm items-center gap-2">
      <Label htmlFor={placeholder}>Filter by {placeholder}</Label>
      <Input type={filterType} placeholder={placeholder} id={placeholder} value={value} onChange={onChange}/>
    </section>
  )
}
