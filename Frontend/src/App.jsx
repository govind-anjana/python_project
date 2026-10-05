import { useState } from "react";
import heroImg from "./assets/hero.png";
import "./App.css";

const apiRoot = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api"
).replace(/\/+$/, "");


function App() {
  const [mode, setMode] = useState("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [signedInAs, setSignedInAs] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setIsSubmitting(true);
    setFeedback(null);

    try {
      const isSignup = mode === "signup";
      const response = await fetch(
        `${apiRoot}/${isSignup ? "signup" : "login"}/`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            ...(isSignup && { name }),
            email,
            password,
          }),
        },
      );
      const result = await response.json().catch(() => null);
      const expectedMessage = isSignup ? "Signup Success" : "Login Success";

      if (!response.ok || result?.msg !== expectedMessage) {
        throw new Error(
          result?.msg || "Could not complete the request. Please try again.",
        );
      }

      if (isSignup) {
        setMode("login");
        setPassword("");
        setFeedback({
          type: "success",
          message: "Your account is ready. Sign in to continue.",
        });
      } else {
        setSignedInAs(result.name || email);
      }
    } catch (error) {
      setFeedback({
        type: "error",
        message:
          error instanceof TypeError
            ? "Could not reach the server. Check that the Django backend is running."
            : error.message,
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  function changeMode(nextMode) {
    setMode(nextMode);
    setPassword("");
    setFeedback(null);
  }

  if (signedInAs) {
    return (
      <main className="signed-in-screen flex min-h-screen items-center justify-center px-6 py-12">
        <section className="signed-in-content w-full max-w-lg text-center">
          <a
            className="brand-mark mx-auto"
            href="#home"
            aria-label="Layer home"
          >
            <img src={heroImg} alt="" />
          </a>
          <p className="eyebrow mt-8">SIGNED IN</p>
          <h1 className="signed-in-title mt-3">Welcome, {signedInAs}.</h1>
          <p className="mt-4 text-base text-stone-600">
            You’re all set. Your next great idea can start here.
          </p>
          <button
            className="quiet-button mt-8"
            onClick={() => setSignedInAs("")}
            type="button"
          >
            Sign out
          </button>
        </section>
      </main>
    );
  }

  const isSignup = mode === "signup";

  return (
    <main className="auth-layout grid min-h-screen lg:grid-cols-[minmax(400px,0.92fr)_minmax(0,1.08fr)]">
      <section className="auth-panel flex min-h-screen flex-col px-6 py-7 sm:px-12 lg:px-16 xl:px-24">
        <a
          className="brand-lockup inline-flex w-fit items-center gap-3"
          href="#home"
          aria-label="Layer home"
        >
          <span className="brand-mark">
            <img src={heroImg} alt="" />
          </span>
          <span className="brand-name">layer</span>
        </a>

        <div className="auth-content mx-auto flex w-full max-w-md flex-1 flex-col justify-center py-14">
          <p className="eyebrow">YOUR SPACE TO BEGIN</p>
          <h1 className="auth-title mt-3">
            {isSignup ? "Make room for more." : "Good to have you back."}
          </h1>
          <p className="auth-intro mt-3">
            {isSignup
              ? "Create an account and bring your ideas together."
              : "Sign in to pick up right where you left off."}
          </p>

          <div
            className="mode-switch mt-8 grid grid-cols-2"
            role="tablist"
            aria-label="Account access"
          >
            <button
              aria-selected={!isSignup}
              className={`mode-option ${!isSignup ? "is-active" : ""}`}
              onClick={() => changeMode("login")}
              role="tab"
              type="button"
            >
              Sign in
            </button>
            <button
              aria-selected={isSignup}
              className={`mode-option ${isSignup ? "is-active" : ""}`}
              onClick={() => changeMode("signup")}
              role="tab"
              type="button"
            >
              Create account
            </button>
          </div>

          <form className="auth-form mt-7" onSubmit={handleSubmit}>
            {isSignup && (
              <label className="field-label" htmlFor="name">
                Your name
                <input
                  autoComplete="name"
                  className="auth-input mt-2 w-full"
                  id="name"
                  onChange={(event) => setName(event.target.value)}
                  placeholder="Alex Morgan"
                  required
                  value={name}
                />
              </label>
            )}

            <label className="field-label block" htmlFor="email">
              Email address
              <input
                autoComplete="email"
                className="auth-input mt-2 w-full"
                id="email"
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@example.com"
                required
                type="email"
                value={email}
              />
            </label>

            <label className="field-label mt-5 block" htmlFor="password">
              Password
              <span className="password-control mt-2 flex w-full items-center">
                <input
                  autoComplete={isSignup ? "new-password" : "current-password"}
                  className="auth-input min-w-0 flex-1"
                  id="password"
                  minLength={isSignup ? 8 : undefined}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder={
                    isSignup ? "At least 8 characters" : "Enter your password"
                  }
                  required
                  type={showPassword ? "text" : "password"}
                  value={password}
                />
                <button
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  className="password-toggle"
                  onClick={() => setShowPassword((visible) => !visible)}
                  type="button"
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </span>
            </label>

            {feedback && (
              <p className={`form-feedback mt-5 ${feedback.type}`} role="alert">
                {feedback.message}
              </p>
            )}

            <button
              className="submit-button mt-7 w-full"
              disabled={isSubmitting}
              type="submit"
            >
              {isSubmitting
                ? "Please wait…"
                : isSignup
                  ? "Create your account"
                  : "Sign in"}
              {!isSubmitting && <span aria-hidden="true">↗</span>}
            </button>
          </form>

          <p className="form-footnote mt-5">
            {isSignup ? "Already have an account?" : "New to Layer?"}{" "}
            <button
              className="text-link"
              onClick={() => changeMode(isSignup ? "login" : "signup")}
              type="button"
            >
              {isSignup ? "Sign in" : "Create an account"}
            </button>
          </p>
        </div>

        <footer className="auth-footer flex items-center justify-between gap-4">
          <span>© Layer</span>
          <span>Thoughtfully made for your work.</span>
        </footer>
      </section>

      <aside
        className="visual-panel relative hidden min-h-screen overflow-hidden lg:flex"
        aria-label="Layer workspace"
      >
        <div className="visual-grid" aria-hidden="true" />
        <div className="visual-topline relative z-10 flex w-full items-center justify-between">
          <span>IDEAS, IN THEIR ELEMENT</span>
          <span className="visual-index">01 / 03</span>
        </div>
        <div className="visual-center relative z-10 flex flex-1 flex-col items-center justify-center">
          <div className="artwork-stage flex items-center justify-center">
            <img
              className="artwork-image"
              src={heroImg}
              alt="Layered geometric artwork"
            />
            <span className="artwork-caption">
              A little more room to think.
            </span>
          </div>
          <div className="visual-copy mt-12 max-w-xl self-start">
            <p className="eyebrow">LESS CLUTTER. MORE CLARITY.</p>
            <p className="visual-title mt-3">
              Bring your
              <br />
              good ideas together.
            </p>
          </div>
        </div>
        <div className="visual-bottom relative z-10 flex w-full items-center justify-between">
          <span>MADE FOR THE WAY YOU THINK</span>
          <span className="visual-line" />
        </div>
      </aside>
    </main>
  );
}

export default App;
