import {
  PhoneCall
} from "lucide-react";


export default function IncomingCall({
  onAnswer
}) {

  return (

    <div className="card">

      <PhoneCall />

      <h3>
        Incoming protected call
      </h3>

      <p>
        மெய்க்குரல் will automatically
        start voice analysis when
        the VoIP call is answered.
      </p>


      <button
        className="primary-btn"
        onClick={onAnswer}
      >

        Answer & Protect

      </button>

    </div>

  );

}