'use client'
import { useRedirectUser } from "@/utils/redirectUser";
import Image from "next/image";
import { useEffect } from "react";

export default function Home() {
  const { redirectUser } = useRedirectUser();

  useEffect(() => {
      redirectUser();
  }, [redirectUser]);
  return (
    <></>
  )
}
