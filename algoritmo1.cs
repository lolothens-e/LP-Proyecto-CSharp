using System;
using System.Text.RegularExpressions;

class RegexTokenizerTest
{
    static void Main()
    {
        string input = "int value = 42; // This is a comment";
        string pattern = @"\w+|[=;]|\S"; // Match words, operators, symbols

        MatchCollection matches = Regex.Matches(input, pattern);

        Console.WriteLine("Tokens:");
        foreach (Match match in matches)
        {
            Console.WriteLine($"[{match.Value}]");
        }
    }
}
