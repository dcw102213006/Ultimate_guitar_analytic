import numpy as np
import pickle
import copy, sys
from six.moves import xrange

from operator import add

NUM_NOTES=88
def check_data(network, data_set):
    """
    Checks if the format of data_set align with the network
    and return the data as numpy array

    """
    data_input, data_targets = data_set
    assert len(data_input[0]) == network.num_inputs, \
        "ERROR: input size varies from the defined input setting"
    assert len(data_targets[0]) == network.layers[-1][0], \
        "ERROR: output size varies from the defined output setting"

    inputs = np.array([data_point for data_point in data_input])
    targets = np.array([data_target for data_target in data_targets])

    return inputs, targets

def generate_binary_vectors(data_set, target=True):
    """ From two lists of chords (input and target), makes binary vectors
    of fixed lenght with ones at indexes where notes occur, zeros elsewhere
    If target=False, only one list of input chords is expected"""
    if target:
        data_input, data_target = data_set

        input_vectors, target_vectors = [],[]
        for this_data_input, this_data_target in zip(data_input,data_target):
            input_vector = (np.zeros(88))
            target_vector = (np.zeros(88))

            input_vector[this_data_input] = 1.
            target_vector[this_data_target] = 1.
            input_vectors.append(input_vector)
            target_vectors.append(target_vector)

        return list(map(list,input_vectors)),list(map(list,target_vectors))
    else:
        input_vectors = []
        for this_data_input in data_set:
            input_vector = (np.zeros(88))

            input_vector[this_data_input] = 1.
            input_vectors.append(input_vector)

        return list(map(list, input_vectors))



def read_all_data(context_size,full_context=False):
    """
    Generates (input, target) pairs on all four datasets.

    Args:
        context_size: the size of the neighborhood window
        full_context: if True, a chord has only one target consisting of a concatenation of all context
         (neighboring) chords.

    Returns: train, validation, and test data for all four datasets (JSB chorales, piano-midi.de, nottingham and muse)

    """
    files_dict = {}
    files_dict['jsb'] = 'JSB_Chorales.pickle'
    files_dict['piano'] = 'Piano-midi.de.pickle'
    files_dict['nottigham'] = 'Nottingham.pickle'
    files_dict['muse'] = 'MuseData.pickle'

    all_train, all_valid, all_test =  [],[],[]
    all_context_train, all_context_valid, all_context_test = [], [], []

    for d in files_dict:
        train, valid, test = read_data(files_dict[d], context_size,full_context=full_context)
        all_train.extend(train[0])
        all_valid.extend(valid[0])
        all_test.extend(test[0])
        all_context_train.extend(train[1])
        all_context_valid.extend(valid[1])
        all_context_test.extend(test[1])

    return [all_train,all_context_train],[all_valid,all_context_valid], [all_test,all_context_test]

def flatten(file_name):
    """ Given a pickle file containing train, validation and test data returns
    a two lists containing the training and testing pieces flatten into one list of chords
    """
    dataset = pickle.load(open(file_name, 'rb'))
    train_data = dataset['train']
    test_data = dataset['test']

    train_data = [y for x in train_data for y in x]
    test_data = [y for x in test_data for y in x]

    train_data=generate_binary_vectors(train_data,False)
    test_data=generate_binary_vectors(test_data,False)

    return train_data, test_data



def make_chord_context(train_data,test_data,valid_data, context_size, full_context=False, augment=False):
    """"Load file_name and build (inputs, targets) pairs

        Args:

			context_size: the size of the context (number of preceeding and succeeding chords)
			full_context: if true, a training pair has the format (input, [output1,...,output_d]) where d=context_size*2
				if false, return multiple traing pairs with the same input : (input, output1),...,(input, output_d)
			training_data: true if we need to read the training data.
			valid_data: true if we need to read the validation data.
			test_data: true if we need to read the test data. Only one of training_data, valid_data and test_data can be true


		Returns:
			data_set: a list of pairs (input, output) = (chord, context chord(s))

	"""

   
    

    def get_full_context(chords_seq):
        """Gives the context of each chord in the list chords_seq

		Args:
			chords_seq: a list of sequences of chords
		Returns:
			chord_and_context: a list of pairs (chord, [contexts]) for each chord in chords_seq
		"""
        chord , context = [],[]
        m_before = context_size
        empty_before = 0
        m_after = context_size
        empty_after = 0

        size = len(chords_seq)
        for i in range(size):
            # the neighborhood of chords at the beginning or at the end of a sequence is smaller
            if i < m_before:
                m_before = i
                empty_before = context_size - m_before
            elif size - i <= m_after:
                m_after = size - i - 1
                empty_after = context_size - m_after

            neighborhood = []

            for j in range(empty_before):
                neighborhood.append([])
            if (m_before > 0):
                neighborhood.extend(map(list, chords_seq[(i - m_before):i]))
            if (m_after > 0):
                neighborhood.extend(map(list, chords_seq[(i + 1):(i + m_after + 1)]))
            for j in range(empty_after):
                neighborhood.append([])

            #for context_chord in neighborhood:
            #    context_chord.append(EOS_ID)

            chord.append(list(chords_seq[i]))
            context.append(neighborhood)
            m_before = context_size
            m_after = context_size
            empty_after = 0
            empty_before = 0

        return (chord,context)

    def get_contexts(chords_seq):
        """Gives the context of each chord in the list chords_seq

		Args:
			chords_seq: a list of sequences of chords
		Returns:
			chord_and_context: a list of pairs (chord, context_1),...,(chord, context_d) for each
			chord in chords_seq. d in -context_size, ..., -1, 1, ... context_size
		"""
        chords , contexts = [], []
        m_before = context_size
        m_after = context_size

        copy_chords_seq = copy.deepcopy(chords_seq)
        size = len(chords_seq)

        for i in range(size):
            # the neighborhood of chords at the beginning or at the end of a sequence is smaller
            if i < m_before:
                m_before = i
            elif size - i <= m_after:
                m_after = size - i - 1

            if (m_before > 0):
                for context in map(list, copy_chords_seq[(i - m_before):i]):
                    c_j = copy.deepcopy(list(context))
                    #c_j.append(EOS_ID)
                    chords.append(list(chords_seq[i]))
                    contexts.append(c_j)
            if (m_after > 0):

                for context in map(list, chords_seq[(i + 1):(i + m_after + 1)]):
                    c_j = copy.deepcopy(list(context))
                    #c_j.append(EOS_ID)
                    chords.append(list(chords_seq[i]))
                    contexts.append(c_j)

            m_before = context_size
            m_after = context_size

        return (chords,contexts)

    tr_chords, tr_contexts = [],[]
    val_chords, val_contexts = [], []
    te_chords, te_contexts = [], []

    

    

    for seq in train_data:
        for i in range(len(seq)):
            seq[i] = list(map(add, seq[i], [-21] * len(seq[i])))
        if full_context:
            chords, contexts = get_full_context(seq)

        else:
            chords, contexts = get_contexts(seq)
        tr_chords.extend(chords)
        tr_contexts.extend(contexts)

    for seq in valid_data:
        for i in range(len(seq)):
            seq[i] = list(map(add, seq[i], [-21] * len(seq[i])))
        if full_context:
            chords, contexts = get_full_context(seq)

        else:
            chords, contexts = get_contexts(seq)
        val_chords.extend(chords)
        val_contexts.extend(contexts)

    for seq in test_data:
        for i in range(len(seq)):
            seq[i] = list(map(add, seq[i], [-21] * len(seq[i])))
        if full_context:
            chords, contexts = get_full_context(seq)

        else:
            chords, contexts = get_contexts(seq)
        te_chords.extend(chords)
        te_contexts.extend(contexts)

    return [tr_chords,tr_contexts], [val_chords,val_contexts], [te_chords,te_contexts]