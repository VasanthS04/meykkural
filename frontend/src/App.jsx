import React, {
  useEffect,
  useRef,
  useState
} from "react";

import {
  Activity,
  ShieldCheck,
  PhoneCall,
  Mic,
  MicOff,
  Menu,
  X,
  Cpu,
  Waves,
  UserRoundCheck,
  AlertTriangle,
  Lock,
  Zap,
  Radio,
  ChevronRight,
  RefreshCw
} from "lucide-react";

import {
  connectAnalysisSocket
} from "./api/websocket";

import {
  startMicrophone,
  stopMicrophone
} from "./audio/microphone";

import {
  VoIPManager
} from "./voip/voipManager";

import "./styles/dashboard.css";
import "./styles/components.css";
import "./styles/responsive.css";


const initialState = {

  risk: 0,
  speaker: 0,
  connected: false,
  analyzing: false,
  listeningLevel: 0,
  frequencies: [],
  models: {
    aasist: 0,
    wav2vec2: 0,
    rawnet2: 0,
    conformer: 0,
    xlsr: 0
  },
  features: {
    mfcc: 0,
    mel: 0,
    lfcc: 0,
    cqcc: 0,
    pitch: 0,
    energy: 0,
    harmonics: 0,
    pauses: 0
  },
  alert:
    "System ready. Start a protected VoIP session."
};


function getRiskLevel(risk) {

  if (risk >= 70) {
    return ["HIGH", "danger"];
  }

  if (risk >= 35) {
    return ["MEDIUM", "warning"];
  }

  return ["LOW", "safe"];
}


function Score({ value }) {

  const number = Math.round(value || 0);

  const className =
    number >= 70
      ? "danger"
      : number >= 35
        ? "warning"
        : "safe";

  return (
    <span className={`score ${className}`}>
      {number}%
    </span>
  );
}


export default function App() {

  const [page, setPage] =
    useState("monitor");

  const [mobileOpen, setMobileOpen] =
    useState(false);

  const [state, setState] =
    useState(initialState);

  const [history, setHistory] =
    useState([]);

  const [riskPopup, setRiskPopup] =
    useState(null);

  const socketRef =
    useRef(null);

  const runningRef =
    useRef(false);

  const sessionRef =
    useRef(0);

  const sampleRateRef =
    useRef(16000);

  const voipManagerRef =
    useRef(null);

  const lastAlertRef =
    useRef("");

  const popupTimerRef =
    useRef(null);


  const handleAnalysisMessage = (data) => {

    const risk = Number(data.risk ?? 0);
    const notification = data.notification;

    setState(previous => ({
      ...previous,
      risk: Number(data.risk ?? previous.risk),
      speaker: Number(data.speaker ?? previous.speaker),
      models: {
        ...previous.models,
        ...(data.models || {})
      },
      features: {
        ...previous.features,
        ...(data.features || {})
      },
      alert: data.alert || notification?.message || previous.alert,
      connected: true
    }));

    if (typeof data.risk === "number") {
      setHistory(previous => [
        ...previous.slice(-39),
        Number(data.risk)
      ]);
    }

    if (risk >= 30 && notification?.notify_user) {
      const alertKey = `${notification.level}:${Math.round(risk)}`;

      if (lastAlertRef.current !== alertKey) {
        lastAlertRef.current = alertKey;
        setRiskPopup({
          level: notification.level,
          title: notification.title,
          message: notification.message,
          risk
        });

        window.clearTimeout(popupTimerRef.current);
        popupTimerRef.current = window.setTimeout(() => {
          setRiskPopup(null);
        }, 8000);

        if ("Notification" in window && Notification.permission === "granted") {
          new Notification(notification.title, {
            body: `${notification.message} Risk: ${Math.round(risk)}/100`
          });
        }
      }
    }
  };


  const resetAnalysisState = () => {
    setHistory([]);
    setState({
      ...initialState,
      alert: "Analysis refreshed. Ready for a new listening session."
    });
  };


  const handleMicrophoneLevel = ({ level, frequencies }) => {
    setState(previous => ({
      ...previous,
      listeningLevel: level,
      frequencies
    }));
  };


  const startAnalysis = async () => {
    if (runningRef.current) {
      stopAnalysis(false);
    }

    const sessionId = sessionRef.current + 1;
    sessionRef.current = sessionId;

    resetAnalysisState();

    if ("Notification" in window && Notification.permission === "default") {
      Notification.requestPermission().catch(() => {});
    }

    runningRef.current = true;

    setState(previous => ({
      ...previous,
      analyzing: true,
      connected: false,
      alert: "Microphone live analysis started."
    }));

    socketRef.current = connectAnalysisSocket({
      sampleRate: 16000,
      source: "browser",
      onMessage: handleAnalysisMessage,
      onOpen: () => {
        if (sessionRef.current !== sessionId) {
          return;
        }
        socketRef.current?.send(JSON.stringify({
          type: "audio_format",
          sample_rate: sampleRateRef.current
        }));
        setState(previous => ({
          ...previous,
          connected: true,
          alert: "Listening live. Complete voice analysis is running."
        }));
      },
      onError: () => {
        if (sessionRef.current !== sessionId) {
          return;
        }
        setState(previous => ({
          ...previous,
          connected: false,
          alert: "Analysis connection failed. Check that the backend is running."
        }));
      },
      onClose: () => {
        if (sessionRef.current !== sessionId) {
          return;
        }
        setState(previous => ({
          ...previous,
          connected: false
        }));
      }
    });

    try {
      await startMicrophone(
        audioBuffer => {
          if (
            socketRef.current &&
            socketRef.current.readyState === WebSocket.OPEN
          ) {
            socketRef.current.send(audioBuffer);
          }
        },
        handleMicrophoneLevel,
        sampleRate => {
          sampleRateRef.current = sampleRate;
          if (
            socketRef.current &&
            socketRef.current.readyState === WebSocket.OPEN
          ) {
            socketRef.current.send(JSON.stringify({
              type: "audio_format",
              sample_rate: sampleRate
            }));
          }
        }
      );

      if (sessionRef.current !== sessionId || !runningRef.current) {
        stopMicrophone();
      }
    } catch (error) {
      console.error(error);
      runningRef.current = false;
      socketRef.current?.close();
      socketRef.current = null;
      stopMicrophone();

      setState(previous => ({
        ...previous,
        analyzing: false,
        connected: false,
        listeningLevel: 0,
        frequencies: [],
        alert: "Unable to access microphone. Please allow microphone access."
      }));
    }
  };


  const startRemoteCallAnalysis = async () => {

    if (runningRef.current) {
      return;
    }

    const sessionId = sessionRef.current + 1;
    sessionRef.current = sessionId;

    runningRef.current = true;

    setState(previous => ({
      ...previous,
      analyzing: true,
      connected: false,
      alert:
        "Waiting for remote call audio..."
    }));

    socketRef.current = connectAnalysisSocket({
      sampleRate: 48000,
      source: "remote-voip",
      onMessage: handleAnalysisMessage,
      onOpen: () => {
        if (sessionRef.current !== sessionId) {
          return;
        }
        setState(previous => ({
          ...previous,
          connected: true
        }));
      },
      onClose: () => {
        if (sessionRef.current !== sessionId) {
          return;
        }
        setState(previous => ({
          ...previous,
          connected: false
        }));
      }
    });

    try {

      voipManagerRef.current = new VoIPManager({
        onCallStart: () => {
          setState(previous => ({
            ...previous,
            alert:
              "Remote call audio received. Analysis started."
          }));
        },
        onAudio: audioBuffer => {
          if (
            socketRef.current &&
            socketRef.current.readyState ===
              WebSocket.OPEN
          ) {
            socketRef.current.send(audioBuffer);
          }
        }
      });

      await voipManagerRef.current.create();

      if (sessionRef.current !== sessionId || !runningRef.current) {
        voipManagerRef.current?.end();
        voipManagerRef.current = null;
      }

    } catch (error) {

      console.error(error);
      voipManagerRef.current?.end();
      voipManagerRef.current = null;
      runningRef.current = false;
      socketRef.current?.close();
      socketRef.current = null;

      setState(previous => ({
        ...previous,
        analyzing: false,
        connected: false,
        alert:
          "Unable to start remote call analysis."
      }));

    }

  };


  const stopAnalysis = (reset = false) => {

    sessionRef.current += 1;
    runningRef.current = false;

    voipManagerRef.current?.end();
    voipManagerRef.current = null;

    stopMicrophone();
    socketRef.current?.close();

    socketRef.current = null;

    setState(previous => ({
      ...previous,
      analyzing: false,
      listeningLevel: 0,
      frequencies: [],
      connected: false,
      alert: reset
        ? "Protected analysis stopped."
        : "Listening stopped. Final analysis retained."
    }));

  };

  const refreshConnection = () => {
    stopAnalysis(false);
    resetAnalysisState();
  };


  const simulateVoIPCall = () => {

    setState(previous => ({

      ...previous,

      alert:
        "VoIP call connected — automatic voice analysis started."

    }));

    startRemoteCallAnalysis();

  };


  useEffect(() => {
    return () => {
      stopAnalysis();
      window.clearTimeout(popupTimerRef.current);
    };

  }, []);


  const [
    riskText,
    riskClass
  ] = getRiskLevel(state.risk);


  const navigation = [

    [
      "monitor",
      "Live Monitor",
      Activity
    ],

    [
      "analysis",
      "Voice Analysis",
      Waves
    ],

    [
      "models",
      "Model Intelligence",
      Cpu
    ],

    [
      "alerts",
      "Security Alerts",
      AlertTriangle
    ]

  ];


  return (

    <div className="app-shell">

      {riskPopup && (
        <div
          className={`risk-popup ${riskPopup.level.toLowerCase()}`}
          role="alert"
          aria-live="assertive"
        >
          <AlertTriangle size={22} />
          <div>
            <strong>{riskPopup.title}</strong>
            <span>{riskPopup.message}</span>
            <b>Risk score: {Math.round(riskPopup.risk)}/100</b>
          </div>
          <button
            className="icon-btn"
            onClick={() => setRiskPopup(null)}
            aria-label="Dismiss risk alert"
            title="Dismiss risk alert"
          >
            <X size={16} />
          </button>
        </div>
      )}


      {/* SIDEBAR */}

      <aside
        className={
          `sidebar ${
            mobileOpen ? "open" : ""
          }`
        }
      >

        <div className="brand">

          <div className="brand-mark">

            <ShieldCheck size={24} />

          </div>


          <div>

            <b>மெய்க்குரல்</b>

            <span>
              Real Voice
            </span>

          </div>


          <button
            className="icon-btn mobile-x"
            onClick={() =>
              setMobileOpen(false)
            }
          >

            <X />

          </button>

        </div>


        <div className="privacy">

          <Lock size={14} />

          <div>

            <b>
              Privacy Mode
            </b>

            <small>
              Audio processed in memory
            </small>

          </div>

        </div>


        <nav>

          {navigation.map(
            ([id, label, Icon]) => (

              <button

                key={id}

                className={
                  page === id
                    ? "active"
                    : ""
                }

                onClick={() => {

                  setPage(id);

                  setMobileOpen(false);

                }}

              >

                <Icon size={18} />

                <span>
                  {label}
                </span>

                <ChevronRight
                  size={14}
                />

              </button>

            )
          )}

        </nav>


        <div className="sidebar-bottom">

          <div className="status-dot">

            <span />

            Backend:
            {" "}

            {
              state.connected
                ? "Connected"
                : "Ready"
            }

          </div>


          <small>
            Real Voice. Real Trust.
          </small>

        </div>

      </aside>


      {/* MAIN */}

      <main className="main">


        {/* HEADER */}

        <header className="topbar">

          <button
            className="icon-btn mobile-menu"
            onClick={() =>
              setMobileOpen(true)
            }
          >

            <Menu />

          </button>


          <div>

            <span className="eyebrow">
              VOICE SECURITY CENTER
            </span>

            <h1>

              {
                navigation.find(
                  item =>
                    item[0] === page
                )?.[1]
              }

            </h1>

          </div>


          <div className="top-actions">

            <span
              className={
                `connection ${
                  state.connected
                    ? "online"
                    : ""
                }`
              }
            >

              <span />

              {
                state.connected
                  ? "LIVE"
                  : "STANDBY"
              }

            </span>


            <button
              className="icon-btn"
              onClick={refreshConnection}
              title="Refresh connection"
              aria-label="Refresh connection"
            >
              <RefreshCw size={15} />
            </button>

            <button
              className={
                state.analyzing
                  ? "top-listen-btn listening"
                  : "top-listen-btn"
              }
              onClick={
                state.analyzing
                  ? stopAnalysis
                  : startAnalysis
              }
            >

              {state.analyzing ? <MicOff size={15} /> : <Mic size={15} />}

              {state.analyzing ? "Stop Listening" : "Start Listening"}

            </button>

          </div>

        </header>


        {/* LIVE MONITOR */}

        {page === "monitor" && (

          <>

            <section className="hero">

              <div>

                <div className="live-chip">

                  <Radio size={14} />

                  REAL-TIME PROTECTION

                </div>


                <h2>

                  Is this voice
                  {" "}

                  <em>
                    genuine?
                  </em>

                </h2>


                <p>

                  Meykkural continuously
                  evaluates acoustic,
                  spectral, prosodic and
                  speaker-verification
                  signals during your
                  protected VoIP call.

                </p>

              </div>


              <div className="hero-actions">

                {!state.analyzing ? (

                  <button
                    className="primary-btn"
                    onClick={startAnalysis}
                  >

                    <Mic />

                    Analyze Person 1 Voice

                  </button>

                ) : (

                  <button
                    className="danger-btn"
                    onClick={stopAnalysis}
                  >

                    <MicOff />

                    Stop Analysis

                  </button>

                )}


                <button
                  className="secondary-btn"
                  onClick={simulateVoIPCall}
                >

                  <PhoneCall />

                  Simulate VoIP Call

                </button>

              </div>

              <FrequencyRing
                active={state.analyzing}
                level={state.listeningLevel}
                frequencies={state.frequencies}
              />

            </section>


            {/* RISK + SPEAKER */}

            <section className="grid-two">


              <div className="card risk-card">

                <div className="card-title">

                  <span>
                    AUTHENTICITY RISK
                  </span>

                  <span
                    className={
                      `badge ${riskClass}`
                    }
                  >
                    {riskText}
                  </span>

                </div>


                <div className="risk-center">

                  <div
                    className={
                      `risk-ring ${riskClass}`
                    }

                    style={{
                      "--p":
                        `${state.risk * 3.6}deg`
                    }}

                  >

                    <div>

                      <strong>
                        {
                          Math.round(
                            state.risk
                          )
                        }
                      </strong>

                      <small>
                        /100
                      </small>

                      <label>
                        RISK SCORE
                      </label>

                    </div>

                  </div>

                </div>


                <p className="center-note">

                  {state.alert}

                </p>

              </div>


              <div className="card speaker-card">

                <div className="card-title">

                  <span>
                    SPEAKER INTEGRITY
                  </span>

                  <UserRoundCheck
                    size={18}
                  />

                </div>


                <div className="speaker-value">

                  <strong>
                    {
                      Math.round(
                        state.speaker
                      )
                    }%
                  </strong>

                  <Score
                    value={
                      100 -
                      state.speaker
                    }
                  />

                </div>


                <div className="progress">

                  <i
                    style={{
                      width:
                        `${state.speaker}%`
                    }}
                  />

                </div>


                <div className="mini-grid">

                  <div>

                    <small>
                      Speaker Match
                    </small>

                    <b>
                      {
                        Math.round(
                          state.speaker
                        )
                      }%
                    </b>

                  </div>


                  <div>

                    <small>
                      Session
                    </small>

                    <b>
                      {
                        state.analyzing
                          ? "ACTIVE"
                          : "IDLE"
                      }
                    </b>

                  </div>

                </div>


                <div className="model-tag">

                  ECAPA-TDNN

                </div>

              </div>

            </section>


            <ModelSection
              models={state.models}
            />


            <FeatureSection
              features={state.features}
            />


            <div className="grid-two">

              <Waveform
                history={history}
              />

              <RiskTimeline
                history={history}
              />

            </div>


            <AlertPanel
              state={state}
            />

          </>

        )}


        {page === "analysis" && (

          <FeatureSection
            features={state.features}
            expanded
          />

        )}


        {page === "models" && (

          <ModelSection
            models={state.models}
            expanded
          />

        )}


        {page === "alerts" && (

          <AlertPanel
            state={state}
            expanded
          />

        )}

      </main>


      {/* MOBILE CALL BAR */}

      <div className="mobile-call-bar">

        <PhoneCall size={16} />

        <span>

          {
            state.analyzing
              ? "Protected call analysis active"
              : "VoIP protection ready"
          }

        </span>


        <button
          onClick={
            state.analyzing
              ? stopAnalysis
              : startAnalysis
          }
        >

          {
            state.analyzing
              ? "STOP"
              : "START"
          }

        </button>

      </div>

    </div>

  );

}


/* MODEL SECTION */

function ModelSection({
  models,
  expanded = false
}) {

  const names = [

    [
      "aasist",
      "AASIST",
      "Spectro-temporal graph"
    ],

    [
      "wav2vec2",
      "wav2vec2",
      "Speech deepfake detector"
    ],

    [
      "rawnet2",
      "RawNet2",
      "Raw waveform analysis"
    ],

    [
      "conformer",
      "Conformer",
      "Attention encoder"
    ],

    [
      "xlsr",
      "XLS-R",
      "Multilingual representation"
    ],

    [
      "ecapa",
      "ECAPA-TDNN",
      "Speaker verification"
    ]

  ];


  return (

    <section
      className={
        `section ${
          expanded
            ? "expanded"
            : ""
        }`
      }
    >

      <div className="section-head">

        <div>

          <span className="eyebrow">
            MODEL INTELLIGENCE
          </span>

          <h3>
            Detection Ensemble
          </h3>

        </div>

        <Cpu />

      </div>


      <div className="model-grid">

        {names.map(
          ([key, name, description]) => {

            const value =
              Number(
                models[key] || 0
              );


            return (

              <div
                className="model-card"
                key={key}
              >

                <div className="model-icon">

                  <Zap size={17} />

                </div>


                <div className="model-info">

                  <b>
                    {name}
                  </b>

                  <small>
                    {description}
                  </small>

                </div>


                <Score
                  value={value}
                />


                <div className="progress">

                  <i
                    style={{
                      width:
                        `${value}%`
                    }}
                  />

                </div>

              </div>

            );

          }
        )}

      </div>

    </section>

  );

}


/* FEATURE SECTION */

function FeatureSection({
  features,
  expanded = false
}) {

  const items = [

    ["mfcc", "MFCC"],

    ["mel", "Mel-Spectrogram"],

    ["lfcc", "LFCC"],

    ["cqcc", "CQCC"],

    ["pitch", "Pitch"],

    ["energy", "Energy"],

    ["harmonics", "Harmonics"],

    ["pauses", "Pauses"]

  ];


  return (

    <section
      className={
        `section ${
          expanded
            ? "expanded"
            : ""
        }`
      }
    >

      <div className="section-head">

        <div>

          <span className="eyebrow">
            VOICE FORENSICS
          </span>

          <h3>
            Acoustic & Prosodic Signals
          </h3>

        </div>

        <Waves />

      </div>


      <div className="feature-grid">

        {items.map(
          ([key, name]) => {

            const value =
              features[key] || 0;


            return (

              <div
                className="feature"
                key={key}
              >

                <span>
                  {name}
                </span>

                <b>
                  {Math.round(value)}%
                </b>


                <div className="progress">

                  <i
                    style={{
                      width:
                        `${value}%`
                    }}
                  />

                </div>

              </div>

            );

          }
        )}

      </div>

    </section>

  );

}


/* WAVEFORM */

function FrequencyRing({
  active,
  level,
  frequencies
}) {
  const bars = frequencies.length
    ? frequencies.slice(0, 32)
    : Array(32).fill(0);

  return (
    <div
      className={`frequency-ring ${active ? "is-listening" : ""}`}
      style={{ "--audio-level": Math.max(0.08, level) }}
      aria-label={active ? "Listening to live audio" : "Microphone idle"}
    >
      <div className="frequency-ring-core">
        <Radio size={20} />
        <strong>{active ? "LISTENING" : "READY"}</strong>
        <small>{active ? `${Math.round(level * 100)}% signal` : "Live audio"}</small>
      </div>
      <div className="frequency-bars" aria-hidden="true">
        {bars.map((value, index) => (
          <i
            key={index}
            style={{
              "--bar-height": `${16 + (value / 255) * 48}px`,
              "--bar-angle": `${index * (360 / bars.length)}deg`
            }}
          />
        ))}
      </div>
    </div>
  );
}

function Waveform({
  history
}) {

  const canvasRef =
    useRef(null);


  useEffect(() => {

    const canvas =
      canvasRef.current;

    if (!canvas) {
      return;
    }


    const context =
      canvas.getContext("2d");


    const ratio =
      window.devicePixelRatio || 1;


    const width =
      canvas.clientWidth *
      ratio;

    const height =
      canvas.clientHeight *
      ratio;


    canvas.width = width;
    canvas.height = height;


    context.clearRect(
      0,
      0,
      width,
      height
    );


    const values =
      history.length
        ? history
        : [
            8, 18, 12,
            28, 17, 32,
            20, 26, 14,
            24, 12
          ];


    context.beginPath();


    values.forEach(
      (value, index) => {

        const x =
          (
            index /
            (values.length - 1 || 1)
          ) * width;


        const y =
          height / 2 +
          Math.sin(index * 1.8) *
          value *
          2;


        if (index === 0) {
          context.moveTo(x, y);
        } else {
          context.lineTo(x, y);
        }

      }
    );


    context.strokeStyle =
      "#55e6ff";

    context.lineWidth =
      2 * ratio;

    context.stroke();

  }, [history]);


  return (

    <div className="card waveform-card">

      <div className="card-title">

        <span>
          LIVE AUDIO SIGNATURE
        </span>

        <span className="pulse">
          ●
        </span>

      </div>


      <canvas
        ref={canvasRef}
      />

    </div>

  );

}


/* RISK TIMELINE */

function RiskTimeline({
  history
}) {

  const values =
    history.length
      ? history
      : Array(10).fill(0);


  return (

    <div className="card timeline">

      <div className="card-title">

        <span>
          RISK TIMELINE
        </span>

        <small>
          LAST 40 WINDOWS
        </small>

      </div>


      <div className="bars">

        {values.map(
          (value, index) => {

            const className =
              value >= 70
                ? "danger"
                : value >= 35
                  ? "warning"
                  : "";


            return (

              <i
                key={index}
                className={className}
                style={{
                  height:
                    `${Math.max(
                      3,
                      value
                    )}%`
                }}
              />

            );

          }
        )}

      </div>

    </div>

  );

}


/* ALERT */

function AlertPanel({
  state,
  expanded = false
}) {

  const [
    label
  ] =
    getRiskLevel(
      state.risk
    );


  return (

    <section
      className={
        `card alert-panel ${
          expanded
            ? "expanded"
            : ""
        } ${label.toLowerCase()}`
      }
    >

      <div className="alert-icon">

        <AlertTriangle />

      </div>


      <div>

        <span className="eyebrow">
          SECURITY STATUS
        </span>


        <h3>

          {
            state.risk >= 70

              ? "Potential voice-cloning attack detected"

              : state.risk >= 35

                ? "Suspicious voice characteristics"

                : "Voice currently appears low risk"
          }

        </h3>


        <p>
          {state.alert}
        </p>

      </div>


      <div className="alert-right">

        <b>
          {label}
        </b>

        <small>
          Dynamic risk engine
        </small>

      </div>

    </section>

  );

}