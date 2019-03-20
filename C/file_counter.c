#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int ndigits(int n) {
	int ans = 1;
	while(n /= 10) ++ans;
	return ans;
}

int make_int(char *s) {
	int i = 0;
	int ans = 0;
	while(s[i] >= '0' && s[i] <= '9') {
		ans *= 10;
		ans += s[i] - '0';
		++i;
	}

	return ans;
}

int count_files (char *dir) {

	FILE *f;
	char count[11];
	char cmd[5000];

	strcpy(cmd, "/bin/ls ");

	strncat(cmd, dir, 4500);

	strcat(cmd, " | /usr/bin/wc -l");

	f = popen(cmd, "r");

	fgets(count, 10, f);

	pclose(f);

	return make_int(count);
}
