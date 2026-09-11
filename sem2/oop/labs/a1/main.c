//a.Generate the first n prime numbers(n is a given natural number).
//b.Given a vector of numbers, find the longest contiguous subsequence such that any two consecutive elements are relatively prime.

#define _CRT_SECURE_NO_WARNINGS

#include<stdio.h>

//check if the given number is prime
int prime(int n)
{
	if (n < 2 || (n > 2 && n % 2 == 0))
		return 0;
	int d = 3, p = 1;
	while (d * d <= n)
	{
		if (n % d == 0)
		{
			p = 0;
			break;
		}
		d += 2;
	}
	if (p == 1)
		return 1;
	else
		return 0;
}

//generates the first n prime numbers
void generate_prime_numbers(int n)
{
	int cnt = 0;
	int nr = 2;
	while (cnt < n)
	{
		if (prime(nr))
		{
			printf("%d ", nr);
			cnt++;
		}
		nr++;
	}
	printf("\n");
}

//computes the greatest common divisor of 2 numbers
int gcd(int a, int b)
{
	int r;
	while (b)
	{
		r = a % b;
		a = b;
		b = r;
	}
	return a;
}

//checks if 2 numbers are relatively prime, that is, if their greatest common divisor is 1
int relatively_prime(int a, int b)
{
	if (gcd(a, b) == 1)
		return 1;
	else
		return 0;
}


//finds the longest contiguous subsequence in the vector, in which every 2 consecutive numbers
//are relatively prime
void find_subsequence(int v[], int v_len) {
	if (v_len == 0)
		return;

	int max_len = 1;
	int global_start = 0;

	int current_len = 1;
	int current_start = 0;

	for (int i = 0; i < v_len - 1; i++) {
		if (gcd(v[i], v[i + 1]) == 1) {
			current_len++;
		}
		else {
			if (current_len > max_len) {
				max_len = current_len;
				global_start = current_start;
			}
			current_start = i + 1;
			current_len = 1;
		}
	}

	if (current_len > max_len) {
		max_len = current_len;
		global_start = current_start;
	}

	printf("Longest relatively prime subsequence: ");
	for (int i = global_start; i < global_start + max_len; i++) {
		printf("%d ", v[i]);
	}
	printf("\n");
}

void app_menu()
{
	int option, n, v[100];

	while (1)
	{
		printf("Menu\n");
		printf("1. Generate the first n prime numbers.\n");
		printf("2. Given a vector of numbers, find the longest contiguous subsequence such that any two consecutive elements are relatively prime.\n");
		printf("3. Exit!\n");

		//scanf("%d", &option);
		if (scanf("%d", &option) != 1)
		{
			printf("Invalid input! Please enter a number.\n");

			while (getchar() != '\n');

			continue; // restart the loop to show the menu again
		}

		if (option == 3)
		{
			printf("Exiting the program!");
			return;
		}

		switch (option)
		{
		case 1:
			printf("Give the number n: ");
			scanf("%d", &n);
			generate_prime_numbers(n);
			break;
		case 2:
			printf("Give the length of the vector: ");
			scanf("%d", &n);
			printf("Give the elements of the vector: ");
			for (int i = 0; i < n; i++)
			{
				scanf("%d", &v[i]);
			}
			find_subsequence(v, n);
			break;
		default:
			printf("Invalid option! Please try again!");
			break;
		}
	}
}

int main()
{
	app_menu();
	return 0;
}