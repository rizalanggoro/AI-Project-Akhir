import { Button } from "./ui/button";

export default function NavbarComponent() {
  return (
    <>
      <div className="fixed top-0 w-full z-50 h-16 border-b backdrop-blur bg-background/70">
        <div className="max-w-5xl mx-auto h-16 flex items-center">
          <a href="./">
            <Button variant={"link"} className="px-0">
              Artificial Intelligent
            </Button>
          </a>
        </div>
      </div>
    </>
  );
}
