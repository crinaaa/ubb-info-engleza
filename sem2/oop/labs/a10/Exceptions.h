#pragma once
#include<string>
#include<vector>
#include<exception>

class RepositoryException : public std::exception
{
protected:
	std::string message;
public:
	RepositoryException() : message("Repository error.") {}
	RepositoryException(const std::string& message) : message(message) {}
	virtual ~RepositoryException() {}
	virtual const char* what() const noexcept override { return message.c_str(); }
};

class DuplicateException : public RepositoryException
{
public:
	DuplicateException() : RepositoryException("A coat with the same size and colour already exists!") {}
	const char* what() const noexcept override { return message.c_str(); }
};

class NotFoundException : public RepositoryException
{
public:
	NotFoundException() : RepositoryException("No such coat found!") {}
	const char* what() const noexcept override { return message.c_str(); }
};

class ValidationException : public std::exception
{
private:
	std::string message;
public:
	ValidationException(const std::string& message) : message(message) {}
	virtual ~ValidationException() {}
	const char* what() const noexcept override { return message.c_str(); }
};