#include "Lexer.hpp"
#include <cctype>

Lexer::Lexer(const std::string &input)
  : input(input), pos(0), peek(0), line(1) {
  if (input.empty()) {
    peek = EOF_CHAR;
  } else {
    peek = static_cast<unsigned char>(input[0]);
  }
}

void Lexer::advance() {
  if (peek == '\n') ++line;
  // TODO: finish me. The advance() method moves the pointer 'pos' forward by one position. 
  // When the end of the string is reached, set 'peek' to EOF_CHAR.
  // You should use static_cast<unsigned char> to ensure 'peek' stores an unsigned char value.
}

void Lexer::resetPos(int newPos) {
  // TODO: finish me. The resetPos(int newPos) method resets 'pos' to newPos 
  // and updates 'peek' accordingly.
}

DragonLexer::DragonLexer(const std::string &input)
  : Lexer(input) {}

Token DragonLexer::nextToken() {
  if (peek == EOF_CHAR) {
    return Token(TokenType::EOF_T, "EOF", line);
  }

  if (std::isspace(peek)) {
    return WS();
  }

  // TODO: finish me. You need to consider when to call ID()
  
  if (std::isdigit(peek)) {
    return NUMBER();
  }

  int cur = peek;
  switch (cur) {
    // TODO: finish me. You need to consider EQ, NE, LT, LE, GT, GE
    case '(':
      advance(); return Token(TokenType::L_PAREN, "(", line);
    case ')':
      advance(); return Token(TokenType::R_PAREN, ")", line);
    case '{':
      advance(); return Token(TokenType::L_BRACE, "{", line);
    case '}':
      advance(); return Token(TokenType::R_BRACE, "}", line);
    case '[':
      advance(); return Token(TokenType::L_BRACKET, "[", line);
    case ']':
      advance(); return Token(TokenType::R_BRACKET, "]", line);
    case ',':
      advance(); return Token(TokenType::COMMA, ",", line);
    case ';':
      advance(); return Token(TokenType::SEMI, ";", line);
    case '+':
      advance(); return Token(TokenType::PLUS, "+", line);
    case '-':
      advance(); return Token(TokenType::MINUS, "-", line);
    case '*':
      advance(); return Token(TokenType::MUL, "*", line);
    case '/':
      advance(); return Token(TokenType::DIV, "/", line);
    case '.':
      advance(); return Token(TokenType::DOT, ".", line);
    default:
      char ch = static_cast<char>(peek);
      std::string s(1, ch);
      advance();
      return Token(TokenType::UNKNOWN, s, line);
  }
}

Token DragonLexer::WS() {
  // TODO: finish me. The WS() method should consume all whitespace characters (spaces, tabs, newlines)
  return Token(TokenType::WS, " ", ???);
}

Token DragonLexer::ID() {
  // TODO: finish me. The ID() method should consume an identifier or keyword.
}

Token DragonLexer::NUMBER() {
  // TODO: finish me. The NUMBER() method should consume an integer, real number, or scientific notation number.
}
