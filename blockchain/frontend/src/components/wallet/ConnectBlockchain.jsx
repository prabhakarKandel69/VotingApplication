import { NoWalletDetected } from "./NoWalletDetected";
import Modal from "react-modal";

const ConnectBlockchain = () => {
  if (window.ethereum === undefined) {
    return (
      <Modal
        isOpen={true}
        // onAfterOpen={afterOpenModal}
        // onRequestClose={closeModal}
        // style={customStyles}
      >
        <NoWalletDetected />
      </Modal>
    );
  }
};

export default ConnectBlockchain;
