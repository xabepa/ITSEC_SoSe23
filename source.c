// fixed return code which told attackers password length
// removed punishment and reproduceable random seed _
//  which told attacker amount of wrong chars and therefore correct chars based on sleeptime
int compare_key() {
    unsigned int len = strlen(key_input);
    unsigned int correct_len = strlen(correct_key);
    int i, false_key = 0;

    if (len != correct_len) {
        false_key = 1; 
    }

    for (i = correct_len - 1; i >= 0; i--) {
        if (key_input[i] != correct_key[i]) {
            false_key = 1;
        }
    }

    if (false_key == 1) {
        usleep(800000 * 15); // no "random", no info
    }

    return false_key;
}