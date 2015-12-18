import bs4, re


class html_cleanup():

  def __init__(self):
    self.text = None
    self.title = None


  def set_text(self, text):
    self.text = bs4.BeautifulSoup(text, 'lxml')


  def remove_empty_elements(self):
    tag_list = ['tr', 'td', 'u']

    for tag in tag_list:
      tag_elements = self.text(tag)

      # Removes the elements with just whitespace in them.
      for element in tag_elements:
        if element.getText().isspace():
          element.decompose()


  # def consolidate_tag_siblings_same_tagname(self, tag):
  #   for tag_element in self.text(tag):
  #     # Find out if tag has siblings.
  #     if tag_element.find_next_siblings():
  #       # If there are siblings see if their tag is the same
  #       for sibling in tag_element.find_next_siblings():
  #         # If the name is the the same
  #         # then remove the text and place inside tag.
  #         if sibling.name == tag_element.name:
  #           tag_element.append(sibling.extract().get_text())


  def remove_title(self):
    # self.title = re.sub(r'(\s\s+)', r' ',
    #   self.text.title.extract().get_text())
    self.title = self.text.title.extract().get_text()

    # Gets the second table in text which contains the bill.
    self.text = self.text('table')[-1].extract()

    # # Gets the first sentence of the bill.
    # for x in self.text('td'):
    #   chkstring = x.get_text() # TODO: Ask Mark if he wants the text extracted.
    #   b = re.search('[.]',chkstring)
    #   # Replaces weird spaces with normal spacing.
    #   self.title += re.sub(r'(\s\s+)',r' ', chkstring)
    #   if b is not None: # Stops the loop when a period is found.
    #     break


  def remove_space(self, tag):
    tag_element = self.text(tag)[0]

    for element in (list(tag_element.next_siblings) +\
      list(tag_element.previous_siblings)):
        if type(element) == bs4.element.NavigableString:
          element.extract()


  def consolidate_tag_elements(self, rem, tag):

    def rm_tag_str_parent(tag):
      for tag_element in self.text(tag):
        tag_element.unwrap()


    def rm_tag_str_dif_sib(tag):
      # Removes tr tags and puts their strings into other tags.
      for tag_element in self.text(tag):
        # first_element = True

        if tag_element.previous_sibling:# and \
          # tag_element.previous_sibling.name != tag:
          # first_element = False
          previous_sibling = tag_element.previous_sibling
          tag_element.extract()
          string_list = list(tag_element.contents)
          for string in string_list:
            previous_sibling.append(string)

        # if first_element:
        else:
          tag_element.name = 'p'


    if rem == 'parent':
      rm_tag_str_parent(tag)
    elif rem == 'sibling different name':
      rm_tag_str_dif_sib(tag)


  def add_tags(self, tag):
    sec = re.compile("\A(SECTION)")
    sec1 =  re.compile("\A(Sec\.)")
    sec3 = re.compile("\A(SUBCHAPTER)")
    sec4 = re.compile("\A(\(.\))(?!\s?\(.\))")

    regcheck = [
      [sec, 'SECTION', "p"],
      [sec1, "Sec", 'p'],
      [sec3, "Subchapter", "p"],
      [sec4, "list", "li"]]

    # Find each expression and add the classes in the set to it.
    for x in regcheck:
      for tag_element in self.text(tag):
        #check what the first word is
        if re.search(x[0], list(tag_element.stripped_strings)[0]):
          tag_element.name = x[2]
          tag_element['class'] = x[1]


  def remove_allspaces(self):
    self.output = str(self.text)
    # self.output = self.text.prettify()
    self.output = str(self.text).split()
    self.output = ' '.join(self.output)
    # self.output = re.sub(r'\{.+\}\s*', '', self.output)


def htmltext(text):
  ttobj = html_cleanup()
  # Set text
  ttobj.set_text(text)
  # Remove empty elements
  # print(ttobj.text.name)
  ttobj.remove_empty_elements()
  # Consolidate tag_elements, siblings w/ same tag_name: 'u'
  # ttobj.consolidate_tag_siblings_same_tagname('u')
  # Consolidate tag parent td
  ttobj.consolidate_tag_elements('parent', 'td')
  # Remove title
  ttobj.remove_title()
  # Remove space
  ttobj.remove_space('tr')
  # Add tags
  ttobj.add_tags('tr')
  # Consolidate tag_elements, siblings w/ different tag_name than: 'tr'
  ttobj.consolidate_tag_elements('sibling different name', 'tr')
  ttobj.remove_allspaces()
  return ttobj.output
