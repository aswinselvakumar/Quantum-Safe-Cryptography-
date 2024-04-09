import random
quantum_states = {
    "rectilinear": {"0": "|0⟩", "1": "|1⟩"},
    "diagonal": {"0": "|+⟩", "1": "|-⟩"}
}
def alice_prepare_key(length):
    key = ''.join(random.choices('01', k=length))
    return key
def alice_encode_key(key_length):
    alice_basis = random.choices(['rectilinear', 'diagonal'], k=key_length)
    alice_key = alice_prepare_key(key_length)
    encoded_key = [(quantum_states[basis][bit], basis) for bit, basis in zip(alice_key, alice_basis)]
    return encoded_key, alice_key, alice_basis
def bob_measure(encoded_key, alice_basis):
    bob_basis = random.choices(['rectilinear', 'diagonal'], k=len(encoded_key))
    bob_results = []
    for qubit, alice_basis, bob_basis in zip(encoded_key, alice_basis, bob_basis):
        if alice_basis == bob_basis:
            measurement = qubit[0]
        else:
            measurement = random.choice(list(quantum_states[bob_basis].values()))
        bob_results.append((measurement, bob_basis))
    return bob_results
def compare_bases(alice_basis, bob_basis):
    return [alice_basis[i] == bob_basis[i] for i in range(len(alice_basis))]
def reconcile_keys(alice_key, bob_key, matching_bases):
    reconciled_key = [alice_key[i] for i in range(len(alice_key)) if matching_bases[i]]
    return ''.join(reconciled_key)
def bb84_protocol(key_length):
    encoded_key, alice_key, alice_basis = alice_encode_key(key_length)

    bob_results = bob_measure(encoded_key, alice_basis)
    
    matching_bases = compare_bases(alice_basis, [basis for _, basis in bob_results])

    reconciled_key = reconcile_keys(alice_key, [bit for bit, _ in bob_results], matching_bases)
    
    return reconciled_key

if __name__ == "__main__":
    key_length = 10
    shared_key = bb84_protocol(key_length)
    print("Shared key:", shared_key)
