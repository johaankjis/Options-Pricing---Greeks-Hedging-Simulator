"use client"

import type React from "react"

import { Suspense } from "react"
import { useSearchParams } from "next/navigation"

export function ClientLayoutWrapper({
  children,
}: {
  children: React.ReactNode
}) {
  const searchParams = useSearchParams()

  return <Suspense fallback={<div>Loading...</div>}>{children}</Suspense>
}
