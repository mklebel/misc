--
-- Database: `arch_deps`
--

-- --------------------------------------------------------

--
-- Table structure for table `package`
--

CREATE TABLE IF NOT EXISTS `package` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `package_dependency`
--

CREATE TABLE IF NOT EXISTS `package_dependency` (
  `package_id` int(11) NOT NULL,
  `package_dep_id` int(11) NOT NULL,
  UNIQUE KEY `package_id` (`package_id`,`package_dep_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

