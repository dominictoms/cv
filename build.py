import os
import yaml

def main():

	# make sure we're in the right directory
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	# read config file
	with open('config.yaml', 'r') as file:
		config = yaml.safe_load(file.read())

	# select cv profile
	print('Select a profile to use')
	profiles = sorted([f for f in os.listdir('profiles')])
	for i, profile in enumerate(profiles):
		temp_name = profile.replace('.txt', '')
		print(f'{i + 1}. {temp_name}')
	profile = profiles[int(input('> ')) - 1]

	# select cover letter
	print('\nSelect a cover letter to use')
	letters = sorted([f for f in os.listdir('letters')])
	for i, letter in enumerate(letters):
		temp_name = letter.replace('.txt', '')
		print(f'{i + 1}. {temp_name}')
	letter = letters[int(input('> ')) - 1]

	# attempt to get company name and address from shell
	company = input('\nEnter company name\n> ')
	address = input('\nEnter company address\n> ')
	role    = input('\nEnter company role\n> ')

	# write the letter!
	write(config, profile, letter, company, address, role)


def handle_url(url):

	# get url both with and without https
	if 'https://' in url:
		website_text = url.replace('https://', '')
		return url, website_text

	else:
		website_url = 'https://' + url + '/'
		return website_url, url

def build_entry(file):

	# read the yaml file
	with open(file, 'r') as file:
		entry = yaml.safe_load(file.read())

	# define an empty string to store the entry
	entry_content = ''

	# iterate through elements in the entry
	for job in entry:
		role = job['role']
		company = job['company']
		url = handle_url(job['url'])[0]
		start = job['start']
		end = job['end']
		skills = ' \u2022 '.join(job['skills'])
		achievements = job['achievements']

		# build the header as a string
		header = f'''\\infolist{{
		\\href{{{url}}}{{\\textbf{{{company}}}}} {role} & From {start} \\\\
		\\textcolor{{darkgray}}{{{skills}}} & until {end}
		}}
		\\noindent
		\\begin{{itemize}}[leftmargin=*, labelsep=0.5em, itemsep=0pt]
		'''

		# build the achievements list
		achievement_items = '\n'.join([f'\\item {achievement}' for achievement in achievements])

		# combine the element into one string
		job_entry_content = f'''
		{header}
        {achievement_items}
		\\end{{itemize}}
		'''

		# add the element to the entry
		entry_content += job_entry_content + '\n\n'

	# send it back!
	return entry_content


def write(config, profile, letter, company, address, role):

	# open specified letter text file
	with open(f'letters/{letter}', 'r') as file:
		letter = file.read()

	# add company name and address to letter
	letter = letter.replace('<company>', company)
	letter = letter.replace('<address>', address)
	letter = letter.replace('<role>', role)

	# store the letter raw text for a text file output
	letter_txt = f'{company}\n{address}\n\n{letter}'

	# remove all whitespace
	split_letter = letter.split('\n')
	split_letter = [para for para in split_letter if para != '']

	# convert list to letter string
	final_letter = '\n\\\\ \\\\\n'.join(split_letter)

	# get url of websites
	website_url, website_text = handle_url(config['website'])
	linkedin_url, linkedin_text = handle_url(config['linkedin'])
	github_url, github_text = handle_url(config['github'])

	# get cv profile
	with open(f'profiles/{profile}', 'r') as file:
		profile = file.read()

	# generate the careers and education from yaml
	careers = build_entry('careers.yaml')
	education = build_entry('education.yaml')

	# dictionary for replacements in cv
	replacements = {
		'company': company,
		'address': address,
		'content': final_letter,
		'name': config['name'],
		'websiteurl': website_url,
		'websitetext': website_text,
		'linkedinurl': linkedin_url,
		'linkedintext': linkedin_text,
		'githuburl': github_url,
		'githubtext': github_text,
		'emailurl': 'mailto:' + config['email'],
		'emailtext': config['email'],
		'careers': careers,
		'education': education,
		'profile': profile
	}

	# open the latex files
	with open('latex/cover.tex', 'r') as file:
		cover_latex = file.read()

	with open('latex/cv.tex', 'r') as file:
		cv_latex = file.read()

	# replace placeholders in latex file
	for replacement in replacements.keys():
		replacement_tag = f'<{replacement}>'
		if replacement_tag in cover_latex:
			cover_latex = cover_latex.replace(replacement_tag, replacements[replacement])

		if replacement_tag in cv_latex:
			cv_latex = cv_latex.replace(replacement_tag, replacements[replacement])

	# filenames for temp files
	temp_cover_name = 'temp_cover.tex'
	temp_cv_name = 'temp_cv.tex'

	# create temp latex files with replacements
	with open(f'latex/{temp_cover_name}', 'w') as file:
		file.write(cover_latex)

	with open(f'latex/{temp_cv_name}', 'w') as file:
		file.write(cv_latex)

	# recreate output directory
	os.system('rm -rf output; mkdir output')

	# write cover letter as plain text
	with open('output/cover.txt', 'w') as file:
		file.write(letter_txt)

	# change to latex folder
	os.chdir('latex')

	# compile the cv and cover letter
	os.system(f'latexmk -pdf -interaction=nonstopmode -output-directory=../output -jobname=cv {temp_cv_name}')
	os.system(f'latexmk -pdf -interaction=nonstopmode -output-directory=../output -jobname=cover {temp_cover_name}')

	# cleanup
	os.system(f'rm {temp_cover_name} {temp_cv_name}')
	os.chdir('../output')
	os.system('rm *.aux *.fdb_latexmk *.fls *.log *.out')

	# merge into one
	os.system('pdftk cv.pdf cover.pdf cat output cvcover.pdf')

if __name__ == '__main__':
	main()
