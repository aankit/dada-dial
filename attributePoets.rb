#!/usr/bin/env ruby
require 'twilio-ruby'
require 'fileutils'

if (ARGV.size > 0)
	numbertocall = ARGV[0]
	message = ARGV[1]
else
	puts "USAGE: gencallfile.rb [phone-number] [context] [exten] [varname=value] [hour-minute-second-month-day-year]\n"
	exit(1)
end

@account_sid = 'AC9b6366875e0812d52136dde85123220c'
@auth_token = 'ccfca6b9380fe50b4c943d2d66ee6153'
@from_number = '19173380048'
@to_number = numbertocall
# set up a client to talk to the Twilio REST API
@client = Twilio::REST::Client.new(@account_sid, @auth_token)

@account = @client.account
@message = @account.messages.create({:from => @from_number, :to => @to_number, :body => message})
puts @message