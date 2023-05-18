variable "username" {

    default = "daniella"
    type = string
  
}

variable "password" {

    type = string
    sensitive = true
  
}

variable "proj-name" {

    default = "web-scraping-data-platform"
    type = string

}